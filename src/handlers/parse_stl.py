import numpy as np
import trimesh


def extract_model_features(stl_path: str, slice_step: float = 0.2) -> dict:
    """
    Анализирует STL-файл и возвращает словарь с геометрическими признаками.
    """
    mesh = trimesh.load(stl_path)
    if mesh.is_empty:
        raise ValueError("STL file is empty or invalid")

    # Общая информация
    bounds = mesh.bounds
    max_height = bounds[1][2] - bounds[0][2]
    bounding_box_volume = mesh.bounding_box.volume

    # --- Минимальная площадь слоя ---
    z_min, z_max = bounds[0][2], bounds[1][2]
    heights = np.arange(z_min + slice_step/2, z_max, slice_step)
    min_area = None

    for z in heights:
        # Получаем сечение на высоте z
        section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if section is None:
            continue
        # section — объект Path3D, преобразуем его в Path2D для получения полигонов
        planar_section, _ = section.to_planar()
        if planar_section is None:
            continue
        total_area = sum(p.area for p in planar_section.polygons_full)
        if min_area is None or total_area < min_area:
            min_area = total_area

    if min_area is None:
        min_area = 0.0

    # --- Максимальный угол свеса ---
    normals = mesh.face_normals
    down_faces = normals[:, 2] < 0
    if np.any(down_faces):
        dot = np.abs(normals[down_faces, 2])
        angles_rad = np.arccos(dot)
        overhang_rad = np.pi/2 - angles_rad
        max_overhang_angle = float(np.degrees(np.max(overhang_rad)))
    else:
        max_overhang_angle = 0.0

    # --- Наличие мостов ---
    has_bridges = False
    if np.any(down_faces):
        overhang_rad = np.pi/2 - np.arccos(np.abs(normals[down_faces, 2]))
        if np.any(overhang_rad > np.deg2rad(80.0)):
            has_bridges = True

    # Толщина стенок — пока не рассчитываем
    min_wall_thickness = None

    return {
        "min_layer_area": round(min_area, 2),
        "max_overhang_angle": round(max_overhang_angle, 2),
        "has_bridges": has_bridges,
        "min_wall_thickness": min_wall_thickness,
        "max_height": round(max_height, 2),
        "bounding_box_volume": round(bounding_box_volume, 2)
    }


def features_to_geometry_settings(features: dict) -> dict:
    """
    Преобразует геометрические признаки STL в настройки слайсера
    """
    settings = {
        "min_layer_area": features["min_layer_area"],
        "max_overhang_angle": features["max_overhang_angle"],
        "has_bridges": features["has_bridges"],
        "min_wall_thickness": features.get("min_wall_thickness"),
        "max_height": features["max_height"],
        "bounding_box_volume": features["bounding_box_volume"],
    }

    min_area = features["min_layer_area"]
    if min_area < 5:
        settings["min_layer_time"] = 15.0
    elif min_area < 20:
        settings["min_layer_time"] = 10.0
    elif min_area < 100:
        settings["min_layer_time"] = 8.0
    else:
        settings["min_layer_time"] = 5.0

    if features["has_bridges"]:
        settings["bridge_speed_multiplier"] = 0.5
        settings["bridge_fan_speed"] = 100
    else:
        settings["bridge_speed_multiplier"] = 1.0
        settings["bridge_fan_speed"] = None

    angle = features["max_overhang_angle"]
    if angle > 50:
        settings["overhang_speed_multiplier"] = 0.6
    elif angle > 30:
        settings["overhang_speed_multiplier"] = 0.7
    else:
        settings["overhang_speed_multiplier"] = 0.9 if angle > 10 else 1.0

    if angle > 45:
        settings["enable_support"] = True
        settings["support_angle_threshold"] = max(45, int(angle) - 5)
        settings["support_type"] = "tree" if min_area < 20 else "normal"
    else:
        settings["enable_support"] = False
        settings["support_angle_threshold"] = 45
        settings["support_type"] = "normal"

    volume = features["bounding_box_volume"]
    if volume > 300000:
        settings["infill_percentage"] = 25
    elif volume > 100000:
        settings["infill_percentage"] = 15
    else:
        settings["infill_percentage"] = 10

    settings["infill_pattern"] = "gyroid" if settings["infill_percentage"] <= 15 else "grid"

    thickness = features.get("min_wall_thickness")
    if thickness is None:
        settings["wall_line_count"] = 2
    elif thickness > 2.0:
        settings["wall_line_count"] = 4
    elif thickness > 1.0:
        settings["wall_line_count"] = 3
    else:
        settings["wall_line_count"] = 2

    height = features["max_height"]
    settings["top_layers"] = 4 if height < 100 else 5
    settings["bottom_layers"] = 3 if height < 100 else 5

    settings["brim_width"] = 3.0 if min_area < 20 else (5.0 if min_area < 100 else 8.0)
    settings["raft_layers"] = 0

    return settings
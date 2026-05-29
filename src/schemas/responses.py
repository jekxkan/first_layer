from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class FilamentSettings(BaseModel):
    """Параметры, зависящие от принтера и пластика."""
    printer_model: str = Field(..., description="Модель принтера")
    printer_nozzle_diameter: float = Field(..., description="Диаметр сопла в мм")
    filament_brand: str = Field(..., description="Бренд пластика")
    filament_type: str = Field(..., description="Тип пластика")
    chamber_temp: int = Field(..., ge=0, le=100, description="Температура термокамеры 0–100°C")
    nozzle_temp_first_layer: int = Field(..., description="Температура сопла для первого слоя")
    nozzle_temp_other_layers: int = Field(..., description="Температура сопла для остальных слоёв")
    bed_temp_first_layer: int = Field(..., description="Температура стола первый слой")
    bed_temp_other_layers: int = Field(..., description="Температура стола остальные слои")
    bed_temp_initial: int = Field(..., description="Начальная температура стола (для градиентного нагрева)")
    bed_temp_final: int = Field(..., description="Финальная температура стола")

    # Охлаждение
    fan_min_speed: Optional[int] = Field(None, description="Мин. скорость вентилятора (%)")
    fan_min_layer_time: Optional[int] = Field(None, description="Время слоя (сек) для мин. скорости вентилятора")
    fan_max_speed: Optional[int] = Field(None, description="Макс. скорость вентилятора (%)")
    fan_max_layer_time: Optional[int] = Field(None, description="Время слоя (сек) для макс. скорости вентилятора")
    fan_always_on: bool = Field(..., description="Вентилятор включен всегда")
    slow_down_for_cooling: bool = Field(..., description="Замедлять печать для охлаждения")

    # Ретракты
    retraction_distance: Optional[float] = Field(None, description="Длина отката в мм")
    retraction_speed: Optional[float] = Field(None, description="Скорость отката в мм/с")

    # Скорости
    print_speed_first_layer: Optional[float] = Field(None, description="Скорость первого слоя в мм/с")
    print_speed_other_layers: Optional[float] = Field(None, description="Скорость остальных слоёв в мм/с")

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class GeometrySettings(BaseModel):
    """Параметры, зависящие от геометрии модели."""
    min_layer_area: Optional[float] = Field(None, description="Минимальная площадь слоя (мм²)")
    max_overhang_angle: Optional[float] = Field(None, description="Максимальный угол свеса в градусах")
    has_bridges: bool = Field(False, description="Есть ли мосты")
    min_wall_thickness: Optional[float] = Field(None, description="Минимальная толщина стенки (мм)")
    max_height: Optional[float] = Field(None, description="Общая высота модели (мм)")
    bounding_box_volume: Optional[float] = Field(None, description="Объём ограничивающего параллелепипеда (мм³)")

    min_layer_time: Optional[float] = Field(None, description="Минимальное время слоя (сек)")
    bridge_speed_multiplier: float = Field(1.0, description="Множитель скорости на мостах")
    bridge_fan_speed: Optional[int] = Field(None, description="Скорость вентилятора на мостах (%)")
    overhang_speed_multiplier: float = Field(1.0, description="Множитель скорости для свесов")
    support_angle_threshold: int = Field(45, description="Пороговый угол поддержек (градусы)")
    enable_support: bool = Field(False, description="Генерировать поддержки")
    support_type: str = Field("normal", description="Тип поддержек: normal, tree")
    infill_percentage: int = Field(15, description="Процент заполнения")
    infill_pattern: str = Field("grid", description="Паттерн заполнения")
    wall_line_count: Optional[int] = Field(None, description="Количество периметров")
    top_layers: Optional[int] = Field(None, description="Верхних сплошных слоёв")
    bottom_layers: Optional[int] = Field(None, description="Нижних сплошных слоёв")
    brim_width: Optional[float] = Field(None, description="Ширина каймы (мм)")
    raft_layers: Optional[int] = Field(None, description="Количество слоёв raft")

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class PrinterProfileResponse(FilamentSettings, GeometrySettings):
    """Полный профиль печати, объединяющий параметры принтера, пластика и геометрии."""
    # Все поля уже унаследованы, можно ничего не добавлять
    pass
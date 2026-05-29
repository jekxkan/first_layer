import os
import tempfile

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from configs.database import get_db
from handlers.parse_stl import (extract_model_features,
                                features_to_geometry_settings)
from models.filament_settings import PrinterFilamentProfile
from repository.geometry_settings import GeometrySettingsRepo
from schemas.base_responses import SuccessResponse, ErrorResponse
from schemas.requests import PrinterSettingsRequest
from schemas.responses import PrinterProfileResponse, FilamentSettings, GeometrySettings

router = APIRouter(prefix="/api/v1")

@router.get("/printer-settings",
            response_model=SuccessResponse,
            responses={
                 400: {"description": "Ошибка обработки файла",
                       "model": ErrorResponse},
                 500: {"description": "Внутренняя ошибка сервера",
                       "model": ErrorResponse}
            },
            response_model_exclude_none=True
)
async def get_printer_settings(
    data: PrinterSettingsRequest = Depends(),
    db: Session = Depends(get_db)
):
    # printer_filament_settings_repo = PrinterFilamentSettingsRepo(db)
    # settings = printer_filament_settings_repo.get_settings(data)
    settings = PrinterFilamentProfile(
        **{
            "printer_model": "Creality Ender 3 V2",
            "printer_nozzle_diameter": 0.4,
            "filament_brand": "Creality",
            "filament_type": "PLA",
            "chamber_temp": 0,
            "nozzle_temp_first_layer": 210,
            "nozzle_temp_other_layers": 205,
            "bed_temp_first_layer": 65,
            "bed_temp_other_layers": 60,
            "bed_temp_initial": 60,
            "bed_temp_final": 60,
            "fan_min_speed": 100,
            "fan_min_layer_time": 10,
            "fan_max_speed": 100,
            "fan_max_layer_time": 5,
            "fan_always_on": True,
            "slow_down_for_cooling": True,
            "retraction_distance": 6.0,
            "retraction_speed": 45.0,
            "print_speed_first_layer": 25.0,
            "print_speed_other_layers": 50.0
        }
    )
    settings_dict = FilamentSettings.model_validate(settings).model_dump(exclude_none=True)

    if data.geometry_settings_id:
        geom_settings_repo = GeometrySettingsRepo(db)
        settings_based_on_geom = geom_settings_repo.get_settings_by_id(
            data.geometry_settings_id
        )
        settings_dict.update(
            GeometrySettings.model_validate(
                settings_based_on_geom
            ).model_dump(exclude_none=True)
        )

    return SuccessResponse(data=PrinterProfileResponse(**settings_dict))


@router.post("/load-stl",
             response_model=SuccessResponse,
             responses={
                 400: {"description": "Ошибка обработки файла",
                       "model": ErrorResponse},
                 500: {"description": "Внутренняя ошибка сервера",
                       "model": ErrorResponse}
             }
)
async def load_stl(
    file: UploadFile = File(..., description="STL-файл модели"),
    response_model=SuccessResponse,
    db: Session = Depends(get_db)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        features = extract_model_features(tmp_path)
        settings = features_to_geometry_settings(features)

        geom_settings_repo = GeometrySettingsRepo(db)
        setting = geom_settings_repo.create_setting(settings)

        return SuccessResponse(data={"id": setting.id})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обработки файла: {str(e)}")
    finally:
        os.unlink(tmp_path)
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, ConfigDict


class PrinterSettingsRequest(BaseModel):
    printer_model: str = Query(..., description="Модель принтера")
    nozzle_diameter: float = Query(..., ge=0.1, le=2.0,
                                   description="Диаметр сопла в мм")
    filament_brand: str = Query(..., description="Бренд пластика")
    filament_type: str = Query(..., description="Тип пластика")
    geometry_settings_id: Optional[str] = Query(
        default=None,
        description="ID настройки, связанной с геометрией"
    )
    model_config = ConfigDict(from_attributes=True)
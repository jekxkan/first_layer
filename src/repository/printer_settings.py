from sqlalchemy.orm import Session

from models.filament_settings import PrinterFilamentProfile
from repository.base import BaseRepo
from schemas.requests import PrinterSettingsRequest


class PrinterFilamentSettingsRepo(BaseRepo):
    def __init__(self, session: Session):
        super().__init__(PrinterFilamentProfile, session)

    def get_settings(self, data: PrinterSettingsRequest):
        return self.get_one(
            **{
                "printer_model": data.printer_model,
                "printer_nozzle_diameter": data.printer_nozzle_diameter,
                "filament_brand": data.filament_brand,
                "filament_type": data.filament_type
            }
        )
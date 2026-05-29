from sqlalchemy.orm import Session

from models.filament_settings import GeometrySettings
from repository.base import BaseRepo


class GeometrySettingsRepo(BaseRepo):
    def __init__(self, session: Session):
        super().__init__(GeometrySettings, session)

    def get_settings_by_id(self, setting_id: str):
        return self.get(setting_id)

    def create_setting(self, data: dict):
        return self.create(**data)
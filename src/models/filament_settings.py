from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Integer, Float, String, Boolean,
    DateTime, CheckConstraint, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PrinterFilamentProfile(Base):
    __tablename__ = "printer_filament_profile"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    printer_model: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True, comment="Модель принтера"
    )
    printer_nozzle_diameter: Mapped[float] = mapped_column(
        Float, nullable=False, comment="Диаметр сопла в мм"
    )
    filament_brand: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Бренд пластика"
    )
    filament_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, comment="Тип пластика"
    )
    chamber_temp: Mapped[int] = mapped_column(
        Integer, CheckConstraint('chamber_temp >= 0 AND chamber_temp <= 100'),
        comment="Температура термокамеры 0–100°C"
    )
    nozzle_temp_first_layer: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Температура сопла для первого слоя"
    )
    nozzle_temp_other_layers: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Температура сопла для остальных слоёв"
    )

    bed_temp_first_layer: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Температура стола первый слой"
    )
    bed_temp_other_layers: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Температура стола остальные слои"
    )
    bed_temp_initial: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Начальная температура стола (для градиентного нагрева)"
    )
    bed_temp_final: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Финальная температура стола"
    )
    fan_min_speed: Mapped[int] = mapped_column(
        Integer, comment="Мин. скорость вентилятора (%)"
    )
    fan_min_layer_time: Mapped[int] = mapped_column(
        Integer, comment="Время слоя (сек) для мин. скорости вентилятора"
    )
    fan_max_speed: Mapped[int] = mapped_column(
        Integer, comment="Макс. скорость вентилятора (%)"
    )
    fan_max_layer_time: Mapped[int] = mapped_column(
        Integer, comment="Время слоя (сек) для макс. скорости вентилятора"
    )
    fan_always_on: Mapped[bool] = mapped_column(
        Boolean, nullable=False, comment="Вентилятор включен всегда"
    )
    slow_down_for_cooling: Mapped[bool] = mapped_column(
        Boolean, nullable=False, comment="Замедлять печать для охлаждения"
    )

    retraction_distance: Mapped[float] = mapped_column(
        Float, comment="Длина отката в мм"
    )
    retraction_speed: Mapped[float] = mapped_column(
        Float, comment="Скорость отката в мм/с"
    )
    print_speed_first_layer: Mapped[float] = mapped_column(
        Float, comment="Скорость первого слоя в мм/с"
    )
    print_speed_other_layers: Mapped[float] = mapped_column(
        Float, comment="Скорость остальных слоёв в мм/с"
    )

    usage_count: Mapped[int] = mapped_column(
        Integer, comment="Сколько раз использовали этот профиль"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class GeometrySettings(Base):
    __tablename__ = "geometry_settings"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    min_layer_area: Mapped[float] = mapped_column(
        Float, comment="Минимальная площадь слоя (мм²)"
    )
    max_overhang_angle: Mapped[float] = mapped_column(
        Float, nullable=True, comment="Максимальный угол свеса в градусах"
    )
    has_bridges: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Есть ли мосты"
    )
    min_wall_thickness: Mapped[float] = mapped_column(
        Float, nullable=True, comment="Минимальная толщина стенки (мм)"
    )
    max_height: Mapped[float] = mapped_column(
        Float, comment="Общая высота модели (мм)"
    )
    bounding_box_volume: Mapped[float] = mapped_column(
        Float, comment="Объём ограничивающего параллелепипеда (мм³)"
    )
    min_layer_time: Mapped[float] = mapped_column(
        Float, nullable=True, comment="Минимальное время слоя (сек)"
    )
    bridge_speed_multiplier: Mapped[float] = mapped_column(
        Float, default=1.0, comment="Множитель скорости на мостах"
    )
    bridge_fan_speed: Mapped[int] = mapped_column(
        Integer, nullable=True, comment="Скорость вентилятора на мостах (%)"
    )
    overhang_speed_multiplier: Mapped[float] = mapped_column(
        Float, default=1.0, comment="Множитель скорости для свесов"
    )
    support_angle_threshold: Mapped[int] = mapped_column(
        Integer, default=45, comment="Пороговый угол поддержек (градусы)"
    )
    enable_support: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Генерировать поддержки"
    )
    support_type: Mapped[str] = mapped_column(
        String(20), default="normal", comment="Тип поддержек: normal, tree"
    )
    infill_percentage: Mapped[int] = mapped_column(
        Integer, default=15, comment="Процент заполнения"
    )
    infill_pattern: Mapped[str] = mapped_column(
        String(30), default="grid", comment="Паттерн заполнения"
    )
    wall_line_count: Mapped[int] = mapped_column(
        Integer, nullable=True, comment="Количество периметров"
    )
    top_layers: Mapped[int] = mapped_column(
        Integer, nullable=True, comment="Верхних сплошных слоёв"
    )
    bottom_layers: Mapped[int] = mapped_column(
        Integer, nullable=True, comment="Нижних сплошных слоёв"
    )
    brim_width: Mapped[float] = mapped_column(
        Float, nullable=True, comment="Ширина каймы (мм)"
    )
    raft_layers: Mapped[int] = mapped_column(
        Integer, nullable=True, comment="Количество слоёв raft"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
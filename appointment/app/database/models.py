from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AppointmentTable(Base):
    """Таблица записей к врачу"""
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    doctor_id: Mapped[int] = mapped_column(nullable=False)
    patient_id: Mapped[int] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

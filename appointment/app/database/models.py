from datetime import datetime, date
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database.base import Base


# class PatientsTable(Base):
#     """Таблица пациентов"""
#     __tablename__ = 'patients'
#     id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
#     first_name: Mapped[str] = mapped_column(nullable=False)
#     last_name: Mapped[str] = mapped_column(nullable=False)
#     birthday: Mapped[date] = mapped_column(nullable=False)
#     gender: Mapped[str] = mapped_column(nullable=False)
#
#     appointments: Mapped[list['AppointmentTable']] = relationship('AppointmentTable', back_populates='patient')
#
#
# class DoctorsTable(Base):
#     """Таблица врачей"""
#     __tablename__ = 'doctors'
#     id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
#     first_name: Mapped[str] = mapped_column(nullable=False)
#     last_name: Mapped[str] = mapped_column(nullable=False)
#     birthday: Mapped[date] = mapped_column(nullable=False)
#     gender: Mapped[str] = mapped_column(nullable=False)
#     specialization: Mapped[str] = mapped_column(nullable=False)
#
#     appointments: Mapped[list['AppointmentTable']] = relationship('AppointmentTable', back_populates='doctor')


class AppointmentTable(Base):
    """Таблица записей к врачу"""
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    # doctor_id: Mapped[UUID] = mapped_column(ForeignKey('doctors.id'), nullable=False)
    # patient_id: Mapped[UUID] = mapped_column(ForeignKey('patients.id'), nullable=False)
    doctor_id: Mapped[int] = mapped_column(nullable=False)
    patient_id: Mapped[int] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    # Уникальное ограничение для пары doctor_id + start_time
    # __table_args__ = (
    #     {'unique_constraint': ('doctor_id', 'start_time')},
    # )

    # patient: Mapped['PatientsTable'] = relationship(PatientsTable, back_populates='appointments')
    # doctor: Mapped['DoctorsTable'] = relationship(DoctorsTable, back_populates='appointments')

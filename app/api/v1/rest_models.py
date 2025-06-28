from datetime import date, datetime, time, timedelta
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.config import settings
from app.core.custom_logger import logger
from app.exceptions.exceptions import IncorrectAppointmentTimeException


class AppointmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    doctor_id: int
    patient_id: int
    start_time: datetime
    end_time: datetime
    description: str | None = Field(default=None, max_length=200)


class AppointmentCreateSchema(BaseModel):
    doctor_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime | None = Field(default=None, description="Передавать этот параметр не обязательно")
    description: str | None = Field(default=None, max_length=200)

    @staticmethod
    def get_high_time(work_end: str, appointment_minutes: int) -> time:
        high_time_range = datetime.strptime(work_end, "%H:%M").time()
        combined_high_time_range = datetime.combine(datetime.today(), high_time_range)
        dt_minus = combined_high_time_range - timedelta(minutes=appointment_minutes)
        return dt_minus.time()

    @model_validator(mode="before")
    @classmethod
    def validate_times(cls, data: Any):
        if isinstance(data, dict):
            work_start = settings.WORK_START
            work_end = settings.WORK_END
            appoint_minutes = settings.APPOINTMENTS_INTERVAL_MINUTES
            start_time = datetime.strptime(data.get("start_time"), "%Y-%m-%d %H:%M:%S")

            if start_time < datetime.now():
                logger.warning(f"Incorrect start time {start_time} while now {datetime.now()}")
                raise IncorrectAppointmentTimeException("Нельзя записаться в прошлое!")
            if start_time.time() < datetime.strptime(work_start, "%H:%M").time():
                logger.warning(f"Incorrect start time: {start_time}. It should be over than {work_start}")
                raise IncorrectAppointmentTimeException(f"Записаться можно с {work_start}")
            result_high_time = cls.get_high_time(work_end=work_end, appointment_minutes=appoint_minutes)
            if start_time.time() > result_high_time:
                logger.warning(f"Incorrect start time: '{start_time}'. It should be less than {result_high_time}")
                raise IncorrectAppointmentTimeException(f"Записаться можно до {result_high_time}")
            if start_time.minute % appoint_minutes != 0 or start_time.second != 0:
                logger.warning(f"Incorrect start time {start_time}: must be a multiple of {appoint_minutes}")
                raise IncorrectAppointmentTimeException(
                    f"""Запись можно делать на каждые {appoint_minutes} минут. Например start_time = 2025-06-28 10:{'00' if appoint_minutes == 60 else appoint_minutes}:00"""
                )
            rounded_minute = (start_time.minute // appoint_minutes) * appoint_minutes
            start_time = start_time.replace(minute=rounded_minute, second=0, microsecond=0)
            data["end_time"] = start_time + timedelta(minutes=appoint_minutes)
            data["start_time"] = start_time
            return data


class AvailableAppointmentsSchema(BaseModel):
    doctor_id: int = Field(gt=0)
    target_date: date
    available_appointments: list[str] | None = None

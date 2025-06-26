from datetime import datetime, timedelta
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.core.config import settings
from app.core.custom_logger import logger


class AppointmentSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
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

    @model_validator(mode='before')
    @classmethod
    def validate_times(cls, data: Any):
        if isinstance(data, dict):
            start_time = datetime.strptime(data.get('start_time'), "%Y-%m-%d %H:%M:%S")
            if start_time < datetime.now():
                logger.warning(f'Incorrect start time {start_time} while now {datetime.now()}')
                raise ValueError('Нельзя записаться в прошлое :)')
            if start_time.minute % settings.APPOINTMENTS_INTERVAL_MINUTES != 0 or start_time.second != 0:
                logger.warning(
                    f"Incorrect start time {start_time}: must be a multiple of {settings.APPOINTMENTS_INTERVAL_MINUTES}"
                )
                raise ValueError(
                    f"""Записать можно делать на каждые {settings.APPOINTMENTS_INTERVAL_MINUTES} минут. Например start_time = 2025-06-28 10:{'00' if settings.APPOINTMENTS_INTERVAL_MINUTES == 60 else settings.APPOINTMENTS_INTERVAL_MINUTES}:00"""
                )
            rounded_minute = (start_time.minute // settings.APPOINTMENTS_INTERVAL_MINUTES) * settings.APPOINTMENTS_INTERVAL_MINUTES
            start_time = start_time.replace(minute=rounded_minute, second=0, microsecond=0)
            data['end_time'] = start_time + timedelta(minutes=settings.APPOINTMENTS_INTERVAL_MINUTES)
            data['start_time'] = start_time
            return data



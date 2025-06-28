from datetime import date, datetime, timedelta

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.rest_models import AppointmentCreateSchema, AppointmentSchema, AvailableAppointmentsSchema
from app.core.config import settings
from app.core.custom_logger import logger
from app.database.connection import get_async_session
from app.database.models import AppointmentTable
from app.exceptions.exceptions import (
    AppointmentAlreadyExistsException,
    AppointmentNotFoundException,
    AvailableAppointmentsNotFoundException,
)


class AppointmentsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_appointment(self, appointment_info: AppointmentCreateSchema) -> AppointmentSchema:
        exist_appointment = await self.session.execute(
            select(AppointmentTable).filter(
                AppointmentTable.doctor_id == appointment_info.doctor_id,
                AppointmentTable.start_time == appointment_info.start_time,
            )
        )
        if exist_appointment.first():
            logger.warning(
                f"Appointment already exists for doctor_id {appointment_info.doctor_id} and start_time {appointment_info.start_time}"
            )
            raise AppointmentAlreadyExistsException(
                doctor_id=appointment_info.doctor_id, start_time=appointment_info.start_time
            )

        new_appointment = AppointmentTable(**appointment_info.model_dump())
        self.session.add(new_appointment)
        await self.session.commit()
        return AppointmentSchema.model_validate(new_appointment)

    async def get_appointment(self, appointment_id: int) -> AppointmentSchema:
        result = await self.session.execute(select(AppointmentTable).filter(AppointmentTable.id == appointment_id))
        record = result.scalar_one_or_none()
        if not record:
            logger.warning(f"Appointment with id {appointment_id} not found")
            raise AppointmentNotFoundException(appointment_id=appointment_id)
        return AppointmentSchema.model_validate(record)

    async def get_available(self, doctor_id: int, target_date: date) -> AvailableAppointmentsSchema:
        work_start = datetime.combine(target_date, datetime.strptime(settings.WORK_START, "%H:%M").time())
        work_end = datetime.combine(target_date, datetime.strptime(settings.WORK_END, "%H:%M").time())

        result = await self.session.execute(
            select(AppointmentTable).filter(
                AppointmentTable.doctor_id == doctor_id,
                AppointmentTable.start_time >= work_start,
                AppointmentTable.start_time < work_end,
            )
        )
        reserved_appointments = result.scalars().all()
        booked_slots = {appoint.start_time for appoint in reserved_appointments}

        all_slots = []  # получение возможных времен для записи к врачу
        new_appointment_time = work_start
        while new_appointment_time < work_end:
            all_slots.append(new_appointment_time)
            new_appointment_time += timedelta(minutes=settings.APPOINTMENTS_INTERVAL_MINUTES)

        available_appointments = [appoint.strftime("%H:%M") for appoint in all_slots if appoint not in booked_slots]
        if not available_appointments:
            logger.warning(f"No available appointments for target date {target_date}")
            raise AvailableAppointmentsNotFoundException

        return AvailableAppointmentsSchema(
            doctor_id=doctor_id, target_date=target_date, available_appointments=available_appointments
        )


def get_appointments_service(session: AsyncSession = Depends(get_async_session)) -> AppointmentsService:
    return AppointmentsService(session=session)

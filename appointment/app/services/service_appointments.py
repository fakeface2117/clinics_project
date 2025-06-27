from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.rest_models import (
    AppointmentCreateSchema,
    AppointmentSchema,
    AvailableAppointmentsSchema
)
from app.core.config import settings
from app.core.custom_logger import logger
from app.database.connection import db_connection
from app.database.models import AppointmentTable
from app.exceptions.exceptions import (
    AppointmentAlreadyExistsException,
    AppointmentNotFoundException,
    AvailableAppointmentsNotFoundException
)


class AppointmentsService:
    @db_connection
    async def add_appointment(
            self,
            session: AsyncSession,
            appointment_info: AppointmentCreateSchema
    ) -> AppointmentSchema:
        exist_appointment = await session.execute(select(AppointmentTable).filter(
            AppointmentTable.doctor_id == appointment_info.doctor_id,
            AppointmentTable.start_time == appointment_info.start_time
        ))
        if exist_appointment.first():
            raise AppointmentAlreadyExistsException(
                doctor_id=appointment_info.doctor_id,
                start_time=appointment_info.start_time
            )

        new_appointment = AppointmentTable(**appointment_info.model_dump())
        session.add(new_appointment)
        await session.commit()
        return AppointmentSchema.model_validate(new_appointment)

    @db_connection
    async def get_appointment(self, session: AsyncSession, appointment_id: int) -> AppointmentSchema:
        result = await session.execute(select(AppointmentTable).filter(AppointmentTable.id == appointment_id))
        record = result.scalar_one_or_none()
        if not record:
            logger.warning(f'Appointment with id {appointment_id} not found')
            raise AppointmentNotFoundException
        return AppointmentSchema.model_validate(record)

    @db_connection
    async def get_available(
            self,
            session: AsyncSession,
            doctor_id: int,
            target_date: date
    ) -> AvailableAppointmentsSchema:
        work_start = datetime.combine(target_date, datetime.strptime("09:00", "%H:%M").time())
        work_end = datetime.combine(target_date, datetime.strptime("18:00", "%H:%M").time())

        result = await session.execute(select(AppointmentTable).filter(
            AppointmentTable.doctor_id == doctor_id,
            AppointmentTable.start_time >= work_start,
            AppointmentTable.start_time < work_end
        ))
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
            doctor_id=doctor_id,
            target_date=target_date,
            available_appointments=available_appointments
        )


def get_appointments_service() -> AppointmentsService:
    return AppointmentsService()

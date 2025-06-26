from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.rest_models import AppointmentCreateSchema, AppointmentSchema
from app.core.custom_logger import logger
from app.database.connection import db_connection
from app.database.models import AppointmentTable
from app.exceptions.exceptions import AppointmentAlreadyExistsException, AppointmentNotFoundException


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


def get_appointments_service() -> AppointmentsService:
    return AppointmentsService()

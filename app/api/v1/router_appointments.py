from datetime import date

from fastapi import APIRouter, Depends

from app.api.v1.rest_models import AppointmentCreateSchema, AppointmentSchema, AvailableAppointmentsSchema
from app.services.service_appointments import AppointmentsService, get_appointments_service

appointments_router = APIRouter()


@appointments_router.post(path="/")
async def new_appointment(
    appointment_info: AppointmentCreateSchema,
    appointments_service: AppointmentsService = Depends(get_appointments_service),
) -> AppointmentSchema:
    """Добавление новой записи пациента к врачу"""
    result = await appointments_service.add_appointment(appointment_info=appointment_info)
    return result


@appointments_router.get(path="/{appointment_id}")
async def get_appointment_info(
    appointment_id: int, appointments_service: AppointmentsService = Depends(get_appointments_service)
) -> AppointmentSchema:
    """Получение информации о записи пациента"""
    appointment_info = await appointments_service.get_appointment(appointment_id=appointment_id)
    return appointment_info


@appointments_router.get(path="/available/{doctor_id}/{target_date}")
async def get_appointment_available(
    doctor_id: int, target_date: date, appointment_service: AppointmentsService = Depends(get_appointments_service)
) -> AvailableAppointmentsSchema:
    """Получение доступных ячеек для записи"""
    available_cells = await appointment_service.get_available(doctor_id=doctor_id, target_date=target_date)
    return available_cells

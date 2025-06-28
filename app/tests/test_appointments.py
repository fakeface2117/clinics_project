from datetime import datetime, timedelta

import pytest

from app.api.v1.rest_models import AppointmentCreateSchema
from app.services.service_appointments import AppointmentsService


@pytest.fixture
def new_appointment():
    appointment_time = datetime.now() + timedelta(days=1)
    appointment_time = str(appointment_time.replace(hour=11, minute=15, second=0, microsecond=0))
    return AppointmentCreateSchema(
        doctor_id=1,
        patient_id=1,
        start_time=appointment_time,
        description="Перелом руки"
    )


async def test_unit_new_appointment(session, new_appointment):
    service = AppointmentsService(session)
    created_appointment = await service.add_appointment(new_appointment)
    assert created_appointment is not None
    assert created_appointment.id == 1
    assert created_appointment.doctor_id == 1
    assert created_appointment.description == "Перелом руки"


async def test_integration_appointments(session, new_appointment):
    service = AppointmentsService(session)
    created_appointment = await service.add_appointment(new_appointment)
    assert created_appointment is not None

    selected_appointment = await service.get_appointment(created_appointment.id)
    assert selected_appointment is not None
    assert created_appointment.id == 1
    assert selected_appointment.doctor_id == 1
    assert created_appointment.description == "Перелом руки"

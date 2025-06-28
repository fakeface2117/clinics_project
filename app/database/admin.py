from sqladmin import ModelView

from app.database.models import AppointmentTable


class AppointmentAdmin(ModelView, model=AppointmentTable):
    column_list = [
        AppointmentTable.id,
        AppointmentTable.doctor_id,
        AppointmentTable.patient_id,
        AppointmentTable.start_time,
        AppointmentTable.end_time,
        AppointmentTable.description,
    ]

from datetime import datetime


class AppError(Exception):
    pass


class NotFoundException(AppError):
    pass


class ConflictException(AppError):
    pass


class AppointmentAlreadyExistsException(ConflictException):
    def __init__(self, doctor_id: int, start_time: datetime):
        self.doctor_id = doctor_id
        self.start_time = start_time
        super().__init__(f'Appointment already exists for doctor {doctor_id} and start time {start_time}')


class AppointmentNotFoundException(NotFoundException):
    def __init__(self, appointment_id: int):
        self.appointment_id = appointment_id
        super().__init__(f'Appointment with id {appointment_id} not found')

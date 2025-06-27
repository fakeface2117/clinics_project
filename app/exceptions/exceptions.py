from datetime import datetime, date


class AppError(Exception):
    pass


class NotFoundException(AppError):
    pass


class ConflictException(AppError):
    pass


class IncorrectDataException(AppError):
    pass


class AppointmentAlreadyExistsException(ConflictException):
    def __init__(self, doctor_id: int, start_time: datetime):
        self.doctor_id = doctor_id
        self.start_time = start_time
        super().__init__(f'Запись уже существует для doctor_id {doctor_id} и start_time {start_time}')


class AppointmentNotFoundException(NotFoundException):
    def __init__(self, appointment_id: int):
        self.appointment_id = appointment_id
        super().__init__(f'Записи с id {appointment_id} не существует')


class AvailableAppointmentsNotFoundException(NotFoundException):
    def __init__(self, target_date: date):
        self.target_date = target_date
        super().__init__(f'Нет доступных записей для выбранной даты {self.target_date}')


class IncorrectAppointmentTimeException(IncorrectDataException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

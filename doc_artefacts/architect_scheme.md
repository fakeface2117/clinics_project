# Архитектурная схема

### 1. Внешние зависимости
- клиенты
- база данных PostgreSQL
### 2. Основные компоненты микросервиса
| **Модуль**                 | **Описание**                                                                                   | **Зависимости**                        | **Пример использования**                         |
|----------------------------|------------------------------------------------------------------------------------------------|----------------------------------------|--------------------------------------------------|
| **FastAPI (API слой)**     | Обрабатывает HTTP-запросы, возвращает ответы.                                                  | `AppointmentsService`, `Pydantic модели` | `POST /appointments` → создание записи           |
| **AppointmentsService**    | Содержит бизнес-логику: создание, просмотр записей по `id`, проверка слотов.                   | `AppointmentsTable`, `Pydantic модели` | `appointment = add_appointment(...)`             |
| **AppointmentsTable**      | Модель SQLAlchemy для работы с таблицей `appointments` в PostgreSQL.                           | `PostgreSQL`, `SQLAlchemy`             | `select(AppointmentsTable).filter(...)`          |
| **Pydantic Models**        | Валидирует входные/выходные данные (DTO).                                                      | `FastAPI`                              | `AppointmentCreateSchema`, `AppointmentSchema`, `AvailableAppointmentsSchema` |
| **Config**                 | Хранит настройки приложения (подключение к БД, переменные окружения).                          | Все модули                             | `DB_CONNECTION_STRING=postgresql://user:pass@db`         |
| **Error Handlers**         | Перехватывает исключения и возвращает структурированные HTTP-ответы.                           | `FastAPI`                              | `HTTP 404 → {"detail": "Запись не найдена"}`     |
| **Docker (Compose)**       | Запускает контейнеры FastAPI приложения и PostgreSQL.                                          | `Docker`, `PostgreSQL`                 | `docker-compose up`                              |
| **CI/CD (GitHub Actions)** | Запускает линтеры (`black`, `flake8`, `isort`) и тесты (`pytest`) перед мержем или пушем кода. | `Makefile`, `pytest`                   | Автоматический запуск при `git push`             |
| **Tests**                  | Юнит- и интеграционные тесты (логика, БД).                                                | `pytest`                 | `test_unit_new_appointment()`                      |
| **Makefile**               | Упрощает запуск задач: линтинг, тесты.                                                         | `black`, `flake8`, `pytest`            | `make lint`, `make test`                         |
![arch.png](arch.png)
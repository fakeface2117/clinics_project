from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from sqladmin import Admin

from app.api.api_metadata import tags_metadata, project_description, project_version, project_title
from app.api.v1.router_appointments import appointments_router
from app.core.config import settings
from app.core.custom_logger import logger, LOGGING_CONFIG
from app.database.admin import AppointmentAdmin
from app.database.connection import create_db, engine
from app.exceptions.exceptions_handlers import exception_handlers


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info('Starting application')
    await create_db()
    logger.info('Database init')
    if settings.MODE == 'DEV':
        logger.info(f'Swagger: {settings.SERVICE_SWAGGER_URL}')
    yield
    logger.info("Stopping application")


app = FastAPI(
    docs_url=f'{settings.SERVICE_BASE_URL}/openapi',
    openapi_url=f'{settings.SERVICE_BASE_URL}/openapi.json',
    lifespan=lifespan,
    exception_handlers=exception_handlers
)
admin = Admin(app, engine)
admin.add_view(AppointmentAdmin)


@app.get('/health')
async def health():
    logger.info('Health check')
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=project_title,
        version=project_version,
        description=project_description,
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(appointments_router, prefix=settings.SERVICE_BASE_URL, tags=['Appointments'])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVICE_LOCAL_HOST,
        port=settings.SERVICE_LOCAL_PORT,
        log_config=LOGGING_CONFIG
    )

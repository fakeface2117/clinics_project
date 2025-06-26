from asyncpg import ConnectionDoesNotExistError
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.custom_logger import logger
from app.exceptions.exceptions import ConflictException, NotFoundException


async def not_found_exception_handler(_: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


async def conflict_exception_handler(_: Request, exc: ConflictException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)}
    )


async def database_connection_exception_handler(_: Request, exc: ConnectionDoesNotExistError) -> JSONResponse:
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database connection error"}
    )


async def database_execute_exception_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database execute query error"}
    )


exception_handlers = {
    NotFoundException: not_found_exception_handler,
    ConflictException: conflict_exception_handler,
    ConnectionDoesNotExistError: database_connection_exception_handler,
    SQLAlchemyError: database_execute_exception_handler
}

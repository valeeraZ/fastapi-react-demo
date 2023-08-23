from fastapi import Request
from fastapi.responses import JSONResponse
from server.exception.base_exception import (
    NotCreatedError,
    NotDeletedError,
    NotFoundError,
    NotUpdatedError,
)


async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content=str(exc),
    )


async def not_created_error_handler(
    request: Request,
    exc: NotCreatedError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=str(exc),
    )


async def not_updated_error_handler(
    request: Request,
    exc: NotUpdatedError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=str(exc),
    )


async def not_deleted_error_handler(
    request: Request,
    exc: NotDeletedError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=str(exc),
    )

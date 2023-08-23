from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from server.exception.base_exception_handler import (
    NotCreatedError,
    NotDeletedError,
    NotFoundError,
    NotUpdatedError,
    not_created_error_handler,
    not_deleted_error_handler,
    not_found_error_handler,
    not_updated_error_handler,
)
from server.web.api import api_router
from server.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="descartes contact list",
        version=metadata.version("server"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # add exception handlers
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(NotCreatedError, not_created_error_handler)
    app.add_exception_handler(NotUpdatedError, not_updated_error_handler)
    app.add_exception_handler(NotDeletedError, not_deleted_error_handler)

    return app

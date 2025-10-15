from importlib import metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from server.web.api.contact import router as contact_router
from server.web.api.monitoring import router as monitoring_router
from server.web.lifetime import lifespan


def _get_version() -> str:
    """Resolve app version from installed metadata or fall back to package constant.

    This avoids importlib.metadata.PackageNotFoundError when running the app
    without installing the project as a distribution.
    """
    try:
        return metadata.version("server")
    except metadata.PackageNotFoundError:
        try:
            # Local fallback defined in server/__init__.py
            import importlib

            mod = importlib.import_module("server")
            return getattr(mod, "__version__", "0.1.0")
        except Exception:
            # Last-resort default
            return "0.1.0"


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="demo contact list",
        version=_get_version(),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include all routers
    app.include_router(contact_router)
    app.include_router(monitoring_router)
    # add exception handlers
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(NotCreatedError, not_created_error_handler)
    app.add_exception_handler(NotUpdatedError, not_updated_error_handler)
    app.add_exception_handler(NotDeletedError, not_deleted_error_handler)

    return app

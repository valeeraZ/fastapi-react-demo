from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from server.infra.db.meta import meta
from server.infra.db.model import load_all_models
from server.settings import settings


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance with optimized
    connection pool settings, session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(
        str(settings.db_url),
        echo=settings.db_echo,
        # Connection pool settings
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_timeout=settings.db_pool_timeout,
        pool_recycle=settings.db_pool_recycle,
        pool_pre_ping=True,  # Validate connections before use
        # Query execution settings
        query_cache_size=1200,  # Size of the query cache
        # Connection arguments passed to asyncpg
        connect_args={
            "server_settings": {
                "search_path": settings.db_schema,
                "timezone": "UTC",
                "application_name": "fastapi_demo_app",
            },
            "command_timeout": settings.db_query_timeout,
            "statement_cache_size": 0,  # Disable prepared statement cache
        },
    )
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


async def _create_tables() -> None:  # pragma: no cover
    """Populates tables in the database with optimized connection settings."""
    load_all_models()
    engine = create_async_engine(
        str(settings.db_url),
        echo=settings.db_echo,
        # Minimal pool for table creation (temporary operation)
        pool_size=1,
        max_overflow=0,
        pool_timeout=30,
        pool_recycle=3600,
        pool_pre_ping=True,
        connect_args={
            "server_settings": {
                "search_path": settings.db_schema,
                "timezone": "UTC",
                "application_name": "fastapi_demo_migration",
            },
            "command_timeout": 300,  # Longer timeout for DDL operations
        },
    )
    async with engine.begin() as connection:
        await connection.run_sync(meta.create_all)
    await engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # pragma: no cover
    """
    Manages the application lifespan.

    This function handles both startup and shutdown events
    using FastAPI's modern lifespan pattern.

    :param app: the fastAPI application.
    :yields: control to the application during its lifetime.
    """
    # Startup
    _setup_db(app)
    await _create_tables()

    yield

    # Shutdown
    await app.state.db_engine.dispose()

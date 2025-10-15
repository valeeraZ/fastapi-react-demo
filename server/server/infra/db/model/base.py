from sqlalchemy.orm import DeclarativeBase

from server.infra.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta

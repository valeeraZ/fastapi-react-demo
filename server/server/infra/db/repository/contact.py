from fastapi import Depends
from server.infra.db.dependencies import get_db_session
from server.infra.db.model.contact_dto import ContactDTO
from server.infra.db.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ContactRepository(BaseRepository[ContactDTO]):
    pass


def get_contact_repository(
    session: AsyncSession = Depends(get_db_session),
) -> ContactRepository:
    """
    Get ContactRepository for dependency injection.

    :param session: the database session from the dependency injection
    :return: a ContactRepository
    """
    return ContactRepository(ContactDTO, session)

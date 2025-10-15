from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.infra.db.dependencies import get_db_session
from server.infra.db.model.contact_dto import ContactDTO
from server.infra.db.repository.base import BaseRepository


class ContactRepository(BaseRepository[ContactDTO]):
    async def get_by_email(self, email: str) -> ContactDTO | None:
        return await self.get(email=email)


def get_contact_repository(
    session: AsyncSession = Depends(get_db_session),
) -> ContactRepository:
    """
    Get ContactRepository for dependency injection.

    :param session: the database session from the dependency injection
    :return: a ContactRepository
    """
    return ContactRepository(ContactDTO, session)

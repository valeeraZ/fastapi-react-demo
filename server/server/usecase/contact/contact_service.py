from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from server.exception.base_exception import NotFoundError
from server.infra.db.model.contact_dto import ContactDTO
from server.infra.db.repository.contact import ContactRepository, get_contact_repository
from server.usecase.contact.contact_model import ContactCreateModel, ContactReadModel


class ContactService:
    def __init__(self, contact_repository: ContactRepository):
        self.contact_repository = contact_repository

    # Commands
    async def create_contact(
        self,
        contact_create_model: ContactCreateModel,
    ) -> ContactReadModel:
        contact_data = contact_create_model.model_dump()
        contact_dto = await self.contact_repository.create(contact_data)
        return ContactReadModel.model_validate(contact_dto)

    # Queries
    async def find_contacts(self) -> list[ContactReadModel]:
        return [
            ContactReadModel.model_validate(contact)
            for contact in await self.contact_repository.get_many()
        ]

    async def find_contact_by_name(self, name: str) -> ContactReadModel:
        contact = await self.contact_repository.get(name=name)
        if contact is None:
            raise NotFoundError(f"Contact {name}")
        return ContactReadModel.model_validate(contact)

    async def find_contact_by_email(self, email: str) -> ContactReadModel:
        contact = await self.contact_repository.get_by_email(email)
        if contact is None:
            raise NotFoundError(f"Contact with email {email}")
        return ContactReadModel.model_validate(contact)

    # Updates (kept for reference/utility)
    async def update_contact_name(
        self,
        session: AsyncSession,
        old_name: str,
        new_name: str,
    ) -> ContactDTO | None:
        stmt = (
            update(ContactDTO)
            .where(ContactDTO.name == old_name)
            .values(name=new_name)
            .returning(ContactDTO)
        )

        result = await session.execute(stmt)
        updated_contact = result.scalar_one_or_none()

        if updated_contact:
            await session.commit()

        return updated_contact

    async def update_contact_name_explicit(
        self,
        session: AsyncSession,
        old_name: str,
        new_name: str,
    ) -> ContactDTO | None:
        contact_stmt = select(ContactDTO).where(ContactDTO.name == old_name)
        result = await session.execute(contact_stmt)
        contact = result.scalar_one_or_none()

        if not contact:
            return None

        try:
            contact.name = new_name
            await session.commit()
            return contact
        except Exception:
            await session.rollback()
            raise

    async def get_contact(self, session: AsyncSession, name: str) -> ContactDTO | None:
        stmt = select(ContactDTO).where(ContactDTO.name == name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


def get_contact_service(
    contact_repository: ContactRepository = Depends(get_contact_repository),
) -> ContactService:
    return ContactService(contact_repository)

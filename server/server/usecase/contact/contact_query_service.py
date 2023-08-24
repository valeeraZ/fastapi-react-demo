from fastapi import Depends
from server.exception.base_exception import NotFoundError
from server.infra.db.repository.contact import ContactRepository, get_contact_repository
from server.usecase.contact.contact_query_model import ContactReadModel


class ContactQuery:
    def __init__(self, contact_repository: ContactRepository):
        self.contact_repository = contact_repository

    async def find_contacts(self) -> list[ContactReadModel]:
        return [
            ContactReadModel.model_validate(contact)
            for contact in await self.contact_repository.get_many()
        ]

    async def find_contact_by_id(self, contact_id: int) -> ContactReadModel:
        contact = await self.contact_repository.get_by_id(contact_id)
        if contact is None:
            raise NotFoundError(f"Contact {contact_id}")
        return ContactReadModel.model_validate(contact)


def get_contact_query_service(
    contact_repository: ContactRepository = Depends(get_contact_repository),
) -> ContactQuery:
    """
    Get ContactQuery service for dependency injection.

    :param contact_repository: the contact repository \
            from the dependency injection
    :return: a ContactQuery service
    """
    return ContactQuery(contact_repository)

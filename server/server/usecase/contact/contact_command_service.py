from fastapi import Depends
from server.infra.db.repository.contact import ContactRepository, get_contact_repository
from server.usecase.contact.contact_command_model import ContactCreateModel
from server.usecase.contact.contact_query_model import ContactReadModel


class ContactCommand:
    def __init__(self, contact_repository: ContactRepository):
        self.contact_repository = contact_repository

    async def create_contact(
        self,
        contact_create_model: ContactCreateModel,
    ) -> ContactReadModel:
        contact_dto = await self.contact_repository.create(
            contact_create_model.model_dump(),
        )
        return ContactReadModel.model_validate(contact_dto)


def get_contact_command_service(
    contact_repository: ContactRepository = Depends(get_contact_repository),
) -> ContactCommand:
    """
    Get ContactCommand service for dependency injection.

    :param contact_repository: the contact repository \
            from the dependency injection
    :return: a ContactCommand service
    """
    return ContactCommand(contact_repository)

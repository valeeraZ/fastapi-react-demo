from fastapi import APIRouter, Depends, status
from server.usecase.contact.contact_command_model import ContactCreateModel
from server.usecase.contact.contact_command_service import (
    ContactCommand,
    get_contact_command_service,
)
from server.usecase.contact.contact_query_model import ContactReadModel
from server.usecase.contact.contact_query_service import (
    ContactQuery,
    get_contact_query_service,
)

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", response_model=ContactReadModel, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_create_model: ContactCreateModel,
    contact_command_service: ContactCommand = Depends(get_contact_command_service),
) -> ContactReadModel:
    """
    Create a contact.

    :param contact_create_model: the schema of the contact to create
    :param contact_command_service: the contact command service \
            from the dependency injection
    :return: a contact read model
    """
    return await contact_command_service.create_contact(contact_create_model)


@router.get(
    "",
    response_model=list[ContactReadModel],
    status_code=status.HTTP_200_OK,
)
async def get_contacts(
    contact_query_service: ContactQuery = Depends(get_contact_query_service),
) -> list[ContactReadModel]:
    """
    Get all contacts.

    :param contact_query_service: the contact query service \
            from the dependency injection
    :return: a list of contact read models
    """
    return await contact_query_service.find_contacts()


@router.get(
    "/{contact_id}",
    response_model=ContactReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_contact_by_id(
    contact_id: int,
    contact_query_service: ContactQuery = Depends(get_contact_query_service),
) -> ContactReadModel:
    """
    Get a contact by id.

    :param contact_id: the id of the contact
    :param contact_query_service: query service \
            from the dependency injection
    :return: a contact read model
    """
    return await contact_query_service.find_contact_by_id(contact_id)

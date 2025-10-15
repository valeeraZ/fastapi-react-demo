from fastapi import APIRouter, Depends, Query, status

from server.usecase.contact.contact_model import ContactCreateModel, ContactReadModel
from server.usecase.contact.contact_service import (
    ContactService,
    get_contact_service,
)

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", response_model=ContactReadModel, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_create_model: ContactCreateModel,
    contact_service: ContactService = Depends(get_contact_service),
) -> ContactReadModel:
    """
    Create a contact.

    :param contact_create_model: the schema of the contact to create
    :param contact_service: the contact service \
            from the dependency injection
    :return: a contact read model
    """
    return await contact_service.create_contact(contact_create_model)


@router.get(
    "",
    response_model=list[ContactReadModel],
    status_code=status.HTTP_200_OK,
)
async def get_contacts(
    contact_service: ContactService = Depends(get_contact_service),
) -> list[ContactReadModel]:
    """Get all contacts."""
    return await contact_service.find_contacts()


@router.get(
    "/by-email",
    response_model=ContactReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_contact_by_email(
    email: str = Query(..., description="Email address of the contact"),
    contact_service: ContactService = Depends(get_contact_service),
) -> ContactReadModel:
    """Get a contact by email address."""
    return await contact_service.find_contact_by_email(email)


@router.get(
    "/{name}",
    response_model=ContactReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_contact_by_name(
    name: str,
    contact_service: ContactService = Depends(get_contact_service),
) -> ContactReadModel:
    """Get a contact by name (primary key)."""
    return await contact_service.find_contact_by_name(name)

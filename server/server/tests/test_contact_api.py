import unittest
from typing import TypedDict, cast
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient
from server.web.api.contact import (
    ContactCreateModel,
    ContactReadModel,
    get_contact_command_service,
    get_contact_query_service,
)
from server.web.application import get_app

ContactDict = TypedDict(
    "ContactDict",
    {
        "id": int,
        "first_name": str,
        "last_name": str,
        "job": str,
        "address": str,
        "question": str,
    },
)

contact_dict_a_create = {
    "first_name": "John",
    "last_name": "Doe",
    "job": "developer",
    "address": "1234 Main St",
    "question": "How do I get started?",
}

contact_dict_a_read: ContactDict = cast(ContactDict, contact_dict_a_create)
contact_dict_a_read["id"] = 1

contact_dict_b_create = {
    "first_name": "Jane",
    "last_name": "Smith",
    "job": "developer",
    "address": "1234 Main St",
    "question": "How do I get started?",
}

contact_dict_b_read: ContactDict = cast(ContactDict, contact_dict_b_create)
contact_dict_b_read["id"] = 2

contact_dicts_read = [contact_dict_a_read, contact_dict_b_read]


class TestContactsAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.app = get_app()

    @patch("server.web.api.contact.get_contact_command_service", new_callable=AsyncMock)
    async def test_create_contact(
        self,
        mock_get_contact_command_service: AsyncMock,
    ) -> None:
        mock_get_contact_command_service.create_contact.side_effect = (
            async_create_contact
        )
        self.app.dependency_overrides = {
            get_contact_command_service: lambda: mock_get_contact_command_service,
        }
        create_model = contact_dict_a_create
        async with AsyncClient(app=self.app, base_url="http://test") as client:
            response = await client.post("/api/contacts", json=create_model)

        mock_get_contact_command_service.create_contact.assert_called_once_with(
            ContactCreateModel(**create_model),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), contact_dict_a_read)
        self.app.dependency_overrides = {}

    @patch(
        "server.usecase.contact.contact_query_service.get_contact_query_service",
        new_callable=AsyncMock,
    )
    async def test_get_contacts(
        self,
        mock_get_contact_query_service: AsyncMock,
    ) -> None:
        mock_get_contact_query_service.find_contacts.side_effect = async_find_contacts

        self.app.dependency_overrides = {
            get_contact_query_service: lambda: mock_get_contact_query_service,
        }
        async with AsyncClient(app=self.app, base_url="http://test") as client:
            response = await client.get("/api/contacts")

        mock_get_contact_query_service.find_contacts.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            contact_dicts_read,
        )
        self.app.dependency_overrides = {}

    @patch(
        "server.usecase.contact.contact_query_service.get_contact_query_service",
        new_callable=AsyncMock,
    )
    async def test_get_contact_by_id(
        self,
        mock_get_contact_query_service: AsyncMock,
    ) -> None:
        mock_get_contact_query_service.find_contact_by_id.side_effect = (
            async_find_contact_by_id
        )

        self.app.dependency_overrides = {
            get_contact_query_service: lambda: mock_get_contact_query_service,
        }
        async with AsyncClient(app=self.app, base_url="http://test") as client:
            response = await client.get("/api/contacts/1")

        mock_get_contact_query_service.find_contact_by_id.assert_called_once_with(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            contact_dict_a_read,
        )
        self.app.dependency_overrides = {}


async def async_create_contact(
    create_model: ContactCreateModel,
) -> ContactReadModel:
    return ContactReadModel(id=1, **create_model.model_dump())


async def async_find_contacts() -> list[ContactReadModel]:
    return [
        ContactReadModel(**contact_dict_a_read),
        ContactReadModel(**contact_dict_b_read),
    ]


async def async_find_contact_by_id(contact_id: int) -> ContactReadModel:
    if contact_id >= len(contact_dicts_read):
        raise IndexError
    return ContactReadModel(**contact_dicts_read[contact_id - 1])


if __name__ == "__main__":
    unittest.main()

import unittest
from typing import TypedDict, cast
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient

from server.web.api.contact import (
    ContactCreateModel,
    ContactReadModel,
    get_contact_service,
)
from server.web.application import get_app


class ContactDict(TypedDict):
    name: str
    email: str
    first_name: str
    last_name: str
    job: str
    address: str


contact_dict_a_create = {
    "name": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "job": "developer",
    "address": "1234 Main St",
}

contact_dict_a_read: ContactDict = cast(ContactDict, contact_dict_a_create)

contact_dict_b_create = {
    "name": "jane_smith",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "job": "developer",
    "address": "1234 Main St",
}

contact_dict_b_read: ContactDict = cast(ContactDict, contact_dict_b_create)

contact_dicts_read = [contact_dict_a_read, contact_dict_b_read]


class TestContactsAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.app = get_app()

    @patch("server.web.api.contact.get_contact_service", new_callable=AsyncMock)
    async def test_create_contact(
        self,
        mock_get_contact_service: AsyncMock,
    ) -> None:
        mock_get_contact_service.create_contact.side_effect = async_create_contact
        self.app.dependency_overrides = {
            get_contact_service: lambda: mock_get_contact_service,
        }
        create_model = contact_dict_a_create
        async with AsyncClient(app=self.app, base_url="http://test") as client:
            response = await client.post("/contacts", json=create_model)

        mock_get_contact_service.create_contact.assert_called_once_with(
            ContactCreateModel(**create_model),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), contact_dict_a_read)
        self.app.dependency_overrides = {}

    @patch("server.web.api.contact.get_contact_service", new_callable=AsyncMock)
    async def test_get_contacts(
        self,
        mock_get_contact_service: AsyncMock,
    ) -> None:
        mock_get_contact_service.find_contacts.side_effect = async_find_contacts

        self.app.dependency_overrides = {
            get_contact_service: lambda: mock_get_contact_service,
        }
        async with AsyncClient(app=self.app, base_url="http://test") as client:
            response = await client.get("/contacts")

        mock_get_contact_service.find_contacts.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            contact_dicts_read,
        )
        self.app.dependency_overrides = {}

    @patch("server.web.api.contact.get_contact_service", new_callable=AsyncMock)
    async def test_get_contact_by_name(
        self,
        mock_get_contact_service: AsyncMock,
    ) -> None:
        mock_get_contact_service.find_contact_by_name.side_effect = (
            async_find_contact_by_name
        )

        self.app.dependency_overrides = {
            get_contact_service: lambda: mock_get_contact_service,
        }
        async with AsyncClient(app=self.app, base_url="http://test") as client:
            response = await client.get("/contacts/john_doe")

        mock_get_contact_service.find_contact_by_name.assert_called_once_with(
            "john_doe",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            contact_dict_a_read,
        )
        self.app.dependency_overrides = {}


async def async_create_contact(
    create_model: ContactCreateModel,
) -> ContactReadModel:
    return ContactReadModel(**create_model.model_dump())


async def async_find_contacts() -> list[ContactReadModel]:
    return [
        ContactReadModel(**contact_dict_a_read),
        ContactReadModel(**contact_dict_b_read),
    ]


async def async_find_contact_by_name(name: str) -> ContactReadModel:
    mapping = {"john_doe": contact_dict_a_read, "jane_smith": contact_dict_b_read}
    return ContactReadModel(**mapping[name])


if __name__ == "__main__":
    unittest.main()

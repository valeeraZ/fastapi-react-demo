import unittest
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient
from server.web.api.contact import (
    ContactCreateModel,
    ContactReadModel,
    get_contact_command_service,
    get_contact_query_service,
)
from server.web.application import get_app

contact_dict_a = {
    "first_name": "John",
    "last_name": "Doe",
    "job": "developer",
    "address": "1234 Main St",
    "question": "How do I get started?",
}

contact_dict_b = {
    "first_name": "Jane",
    "last_name": "Smith",
    "job": "developer",
    "address": "1234 Main St",
    "question": "How do I get started?",
}


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
        create_model = contact_dict_a
        async with AsyncClient(app=self.app, base_url="http://test") as client:
            response = await client.post("/api/contacts/", json=create_model)

        mock_get_contact_command_service.create_contact.assert_called_once_with(
            ContactCreateModel(**create_model),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), create_model)
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
            response = await client.get("/api/contacts/")

        mock_get_contact_query_service.find_contacts.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                contact_dict_a,
                contact_dict_b,
            ],
        )


async def async_create_contact(
    create_model: ContactCreateModel,
) -> ContactReadModel:
    return ContactReadModel(**contact_dict_a)


async def async_find_contacts() -> list[ContactReadModel]:
    return [
        ContactReadModel(**contact_dict_a),
        ContactReadModel(**contact_dict_b),
    ]


if __name__ == "__main__":
    unittest.main()

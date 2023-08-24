"""API for the application."""
from fastapi.routing import APIRouter
from server.web.api import contact, monitoring

api_router = APIRouter()
api_router.include_router(contact.router)
api_router.include_router(monitoring.router)

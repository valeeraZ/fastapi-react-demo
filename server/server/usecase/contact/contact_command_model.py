from pydantic import BaseModel


class ContactCreateModel(BaseModel):
    first_name: str
    last_name: str
    job: str
    address: str
    question: str

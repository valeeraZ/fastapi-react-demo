from pydantic import BaseModel


class ContactReadModel(BaseModel):
    first_name: str
    last_name: str
    job: str
    address: str
    question: str

    class Config:
        from_attributes = True

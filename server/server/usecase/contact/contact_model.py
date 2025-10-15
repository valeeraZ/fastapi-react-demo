from pydantic import BaseModel, EmailStr


class ContactCreateModel(BaseModel):
    name: str  # Primary key
    email: EmailStr
    first_name: str
    last_name: str
    job: str
    address: str


class ContactReadModel(BaseModel):
    name: str  # Primary key instead of id
    email: EmailStr
    first_name: str
    last_name: str
    job: str
    address: str

    class Config:
        from_attributes = True

from pydantic import BaseModel


class Contact_in(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    birthday: str
    text: str = None

class Contact_out(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: str
    birthday: str
    text: str = None

    class Config:
        from_attributes = True

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
    id_user: int

    class Config:
        from_attributes = True

class User_in(BaseModel):
    username: str
    password: str


class User_out(BaseModel):
    id: int
    username: str
    password: str
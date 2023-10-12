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

class UserModel(BaseModel):
    email: str
    password: str

class UserDb(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

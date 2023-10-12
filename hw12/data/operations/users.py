from typing import Optional

from sqlalchemy.orm import Session
from data.db.db_models import User
from data.validation_schemes import UserModel



async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> UserModel:
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    '''new_user = User(
        email=body.email,
        password=body.password,
        refresh_token=body.refresh_token
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user'''


async def update_token(user: User, token: Optional[str], db: Session) -> None:
    user.refresh_token = token
    db.commit()
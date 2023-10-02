from fastapi import FastAPI, Depends, HTTPException, status, Security
from db_models import DBContact, User
from validation_schemes import Contact_in, Contact_out, User_in
from sqlalchemy.orm import Session
from connect_db import get_db
from typing import List
from datetime import timedelta, datetime
from sqlalchemy import extract
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from auth import get_current_user, Hash, create_access_token, create_refresh_token, get_login_from_refresh_token

app = FastAPI()
hash_handler = Hash()
security = HTTPBearer()

@app.post("/signup", tags=['auth'])
async def signup(body: User_in, db: Session = Depends(get_db)):
    exist_user = db.query(User).filter(User.login == body.username).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    new_user = User(login=body.username, password=hash_handler.get_password_hash(body.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.login}


@app.post("/login", tags=['auth'])
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == body.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login")
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_current_user)):
    token = credentials.credentials
    login = await get_login_from_refresh_token(token)
    user = db.query(User).filter(User.login == login).first()
    if user.refresh_token != token:
        user.refresh_token = None
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await create_access_token(data={"sub": login})
    refresh_token = await create_refresh_token(data={"sub": login})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.get("/")
async def root():
    return {"message": "App RUN"}

@app.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": 'secret router', "owner": current_user.login, "id":current_user.id}

@app.get("/contact", response_model = List[Contact_out], tags=['contacts'])
async def show_all_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    show_contact = db.query(DBContact).filter_by(id=current_user.id).all()
    return show_contact

@app.post("/contact", response_model = Contact_out, tags=['contacts'])
async def add_contact(contact: Contact_in, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_contact = DBContact(
        name=contact.name,
        surname=contact.surname,
        email=contact.email,
        phone=contact.phone,
        birthday=contact.birthday,
        text=contact.text,
        id_user=current_user.id
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact
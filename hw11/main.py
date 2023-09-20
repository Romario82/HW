from fastapi import FastAPI, Depends, HTTPException, status
from db_models import DBContact
from validation_schemes import Contact_in, Contact_out
from sqlalchemy.orm import Session
from connect_db import get_db
from typing import List
from datetime import timedelta, date, datetime
from sqlalchemy import extract

app = FastAPI()


@app.post("/contact", response_model = Contact_out, tags=['contacts'])
async def add_contact(contact: Contact_in, db: Session = Depends(get_db)):
    new_contact = DBContact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@app.put("/contact/{id_contact}", response_model = Contact_out, tags=['contacts'])
async def update_contact(contact: Contact_in, id_contact: int, db: Session = Depends(get_db)):
    up_contact = db.query(DBContact).filter_by(id=id_contact).first()
    if up_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    up_contact.name = contact.name
    up_contact.surname = contact.surname
    up_contact.email = contact.email
    up_contact.phone = contact.phone
    up_contact.birthday = contact.birthday
    up_contact.text = contact.text
    db.commit()
    return up_contact

@app.get("/contact", response_model = List[Contact_out], tags=['contacts'])
async def show_all_contacts(db: Session = Depends(get_db)):
    show_contact = db.query(DBContact).all()
    return show_contact

@app.get("/contact/{id_contact}", response_model = Contact_out, tags=['contacts'])
async def show_id_contact(id_contact: int, db: Session = Depends(get_db)):
    showid_contact = db.query(DBContact).filter_by(id=id_contact).first()
    if showid_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return showid_contact

@app.get("/contact/", response_model=Contact_out, tags=['contacts'])
async def search_contacts(search: str, db: Session = Depends(get_db)):
    search_contact = db.query(DBContact).filter(
        (DBContact.name == search) | (DBContact.surname == search) | (DBContact.email == search)
    ).first()
    if search_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return search_contact

@app.get("/contact", response_model = Contact_out, tags=['contacts'])
def birthday_contact(db: Session = Depends(get_db)):
    current_date = datetime.now().date()
    target_date = current_date + timedelta(days=7)
    birthday = db.query(DBContact).filter(
    (extract('month', DBContact.birthday) == current_date.month) &
    (extract('day', DBContact.birthday) >= current_date.day) &
    (extract('day', DBContact.birthday) <= target_date.day)).all()
    return birthday

@app.delete("/contact/{id_contact}", tags=['contacts'])
async def delete_contact(id_contact: int, db: Session = Depends(get_db)):
    del_contact = db.query(DBContact).filter_by(id=id_contact).first()
    if del_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    db.delete(del_contact)
    db.commit()
    return del_contact
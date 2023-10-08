from sqlalchemy import extract
from sqlalchemy.orm import Session
from data.db.db_models import DBContact, User
from data.validation_schemes import Contact_in
from datetime import timedelta, datetime

async def add_contact(contact: Contact_in, user: User, db: Session):
    new_contact = DBContact(
        name=contact.name,
        surname=contact.surname,
        email=contact.email,
        phone=contact.phone,
        birthday=contact.birthday,
        text=contact.text,
        id_user=user.id
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

async def update_contact(contact: Contact_in, id_contact: int, user: User, db: Session):
    up_contact = db.query(DBContact).filter_by(id=id_contact, id_user=user).first()
    up_contact.name = contact.name
    up_contact.surname = contact.surname
    up_contact.email = contact.email
    up_contact.phone = contact.phone
    up_contact.birthday = contact.birthday
    up_contact.text = contact.text
    db.commit()
    return up_contact

async def show_all_contacts(user: User, db: Session):
    show_contact = db.query(DBContact).filter_by(id_user=user).all()
    return show_contact

async def show_id_contact(id_contact: int, user: User, db: Session):
    showid_contact = db.query(DBContact).filter_by(id=id_contact, id_user=user).first()
    return showid_contact

async def search_contacts(search: str, user: User, db: Session):
    search_contact = db.query(DBContact).filter(
        (DBContact.name == search) | (DBContact.surname == search) | (DBContact.email == search)
    ).filter_by(id_user=user).first()
    return search_contact

async def birthday_contact(user: User, db: Session):
    current_date = datetime.now().date()
    target_date = current_date + timedelta(days=7)
    birthday = db.query(DBContact).filter(
    (extract('month', DBContact.birthday) == current_date.month) &
    (extract('day', DBContact.birthday) >= current_date.day) &
    (extract('day', DBContact.birthday) <= target_date.day)
    ).filter_by(id_user=user).all()
    return birthday

async def delete_contact(id_contact: int, user: User, db: Session):
    del_contact = db.query(DBContact).filter_by(id=id_contact, id_user=user).first()
    db.delete(del_contact)
    db.commit()
    return del_contact

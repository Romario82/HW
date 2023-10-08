from fastapi import APIRouter, HTTPException, Depends, status
from data.db.db_models import User
from typing import List
from sqlalchemy.orm import Session
from data.validation_schemes import Contact_in, Contact_out
from data.db.connect_db import get_db
from data.operations import operations_contacts as oper_contact
from data.auth.auth import auth_service

router = APIRouter(prefix="/contact", tags=["contacts"])

@router.post("/", response_model = Contact_out)
async def add_contacts(contact: Contact_in, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await oper_contact.add_contact(contact, current_user, db)

@router.put("/{id_contact}", response_model = Contact_out, tags=['contacts'])
async def update_contact(contact: Contact_in, id_contact: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    up_contact = oper_contact.update_contact(contact, id_contact, current_user, db)
    if up_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return await up_contact

@router.get("/", response_model = List[Contact_out], tags=['contacts'])
async def show_all_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await oper_contact.show_all_contacts(current_user, db)

@router.get("/{id_contact}", response_model = Contact_out, tags=['contacts'])
async def show_id_contact(id_contact: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    showid_contact = oper_contact.show_id_contact(id_contact, current_user, db)
    if showid_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return await showid_contact

@router.get("/search", response_model=Contact_out, tags=['contacts'])
async def search_contacts(search: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    search_contact = oper_contact.search_contacts(search, current_user, db)
    if search_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return await search_contact

@router.get("/contact_birthday", response_model=List[Contact_out], tags=['contacts'])
async def birthday_contact(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await oper_contact.birthday_contact(current_user, db)

@router.delete("/contact/{id_contact}", tags=['contacts'])
async def delete_contact(id_contact: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    del_contact = oper_contact.delete_contact(id_contact, current_user, db)
    if del_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return await del_contact

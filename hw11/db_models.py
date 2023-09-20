from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from connect_db import engine

Base = declarative_base()

class DBContact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    surname = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    birthday = Column(String, nullable=False, index=True)
    text = Column(String, nullable=True, index=True)

Base.metadata.create_all(bind=engine)
if __name__ == '__main__':
    pass
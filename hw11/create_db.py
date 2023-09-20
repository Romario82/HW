import os
from db_models import Contact, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker

fake = Faker("uk_UA")

if not os.path.exists('contacts.db'):
    url_bd = 'sqlite:///contacts.db'
    engine = create_engine(url_bd)
    Base.metadata.create_all(engine)

engine = create_engine("sqlite:///contacts.db")
Session = sessionmaker(bind=engine)
session = Session()




#date_received = fake.date_between(start_date='-4d', end_date='today')

from faker import Faker
from db_models import DBContact
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
import pytz


fake = Faker("uk_UA")
utc_tz = pytz.timezone('UTC')

engine = create_engine("sqlite:///contacts.db")
Session = sessionmaker(bind=engine)
session = Session()

for _ in range(30):
    contacts = DBContact(name = fake.first_name(), surname = fake.last_name(),
                         email = fake.free_email(), phone = fake.phone_number(),
                         birthday = fake.date_of_birth(minimum_age=20, maximum_age=60, tzinfo=utc_tz), text = "")
    session.add(contacts)
session.commit()

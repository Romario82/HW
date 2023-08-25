import pika
import json
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField


connect(host='mongodb+srv://user1_db:zaqwsx@cluster0.840soav.mongodb.net/send_db')


conn_rabbit = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = conn_rabbit.channel()
channel.queue_declare(queue='send_queue')

fake = Faker()

class Contact(Document):
    fullname = StringField()
    email = StringField()
    sent = BooleanField(default=False)


num_contacts = 5
for _ in range(num_contacts):
    contact = Contact(fullname=fake.name(), email=fake.email())
    contact.save()

for contact in Contact.objects():
    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))


print(f"{num_contacts} повідомлень надіслано в чергу")
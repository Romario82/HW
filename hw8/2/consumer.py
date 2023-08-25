import pika
import json
import time
from producer import Contact
from bson import ObjectId


conn_rabbit = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn_rabbit.channel()

channel.queue_declare(queue='email_queue')


def send_email(contact_id):
    print(f"Відправлено повідомлення контакту з ID: {contact_id}")
    time.sleep(2)  # Імітація надсилання


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = ObjectId(message['contact_id'])

    contact = Contact.objects(id=contact_id, sent=False).first()
    if contact:
        send_email(contact_id)
        contact.update(set__sent=True)
        print(f"Повідомлення відправлено контакту з ID: {contact_id}")
    else:
        print(f"Контакт з ID {contact_id} не знайдений або вже відправлено")


channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Очікування повідомлень. Для виходу натисніть Ctrl+C')
channel.start_consuming()
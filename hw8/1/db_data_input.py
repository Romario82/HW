from mongoengine import Document, StringField, ListField, ReferenceField, connect
import json

class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

connect(host='mongodb+srv://user1_db:zaqwsx@cluster0.840soav.mongodb.net/db')

def db_data_input():
    with open('authors.json', 'r') as authors_f:
        authors_data = json.load(authors_f)

    with open('qoutes.json', 'r') as quotes_f:
        quotes_data = json.load(quotes_f)

    for author_data in authors_data:
        Author(**author_data).save()

    for quote_data in quotes_data:
        author_name = quote_data.pop('author')
        author = Author.objects(fullname=author_name).first()
        quote_data['author'] = author
        Quote(**quote_data).save()

if __name__ == '__main__':
    db_data_input()
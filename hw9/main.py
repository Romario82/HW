import requests
import json
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/'


def to_json(file_name, out_list):
    with open(file_name, 'w', encoding='utf-8') as out_file:
        json.dump(out_list, out_file, ensure_ascii=False, indent=2)
    print(f'{file_name} OK!')


def get_quotes():
    quotes_list = []
    autor_list_link = []
    page_num = 1

    while True:
        response = requests.get(f'{url}/page/{page_num}')
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all(class_='quote')
        if not quotes:
            break
        for quote in quotes:
            text = quote.find(class_='text').get_text()
            author = quote.find(class_='author').get_text()
            author_link = quote.find('a').get('href')
            if author_link not in autor_list_link:
                autor_list_link.append(author_link)
            tags = [tag.get_text() for tag in quote.find_all(class_='tag')]
            quotes_list.append({
                "tags": tags,
                "author": author,
                "quote": text
            })
        page_num += 1

    file_name = 'quotes.json'
    to_json(file_name, quotes_list)
    return autor_list_link

def get_autor(links):
    autor_list = []
    for link in links:
        response = requests.get(f'{url}/{link}')
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all(class_='author-details')
        for quote in quotes:
            fullname = quote.find(class_='author-title').get_text()
            born_date = quote.find(class_='author-born-date').get_text()
            born_location = quote.find(class_='author-born-location').get_text()
            description = quote.find(class_='author-description').get_text()
            autor_list.append(
                {'fullname':fullname,
                'born_date':born_date,
                'born_location':born_location,
                'description':description.replace("\n","").strip()
                })
    file_name = 'authors.json'
    to_json(file_name, autor_list)


def main():
    autor_link = get_quotes()
    get_autor(autor_link)

if __name__ == '__main__':
    main()




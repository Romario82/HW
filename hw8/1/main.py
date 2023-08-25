from db_data_input import Author, Quote

def autor(args):
    author_name = ' '.join(args)
    author = Author.objects(fullname=author_name).first()
    quotes = Quote.objects(author=author)
    for quote in quotes:
        print(quote.quote)

def tag(args):
    tag = ' '.join(args)
    quotes = Quote.objects(tags=tag)
    for quote in quotes:
        print(quote.quote)

def tags(args):
    tags = ''.join(args)
    tags = tags.split(','))
    quotes = Quote.objects(tags__in=tags)
    for quote in quotes:
        print(quote.quote)

def no_command(_):
    print('No command!!! Введіть команду autor: ,tag: ,tags: ,exit')

def main():
    command_tags = {'autor': autor, 'tag': tag, 'tags': tags}
    print('Введіть команду autor: ,tag: ,tags: ,exit')
    while True:
        input_command = input('Введіть команду -> ')
        if input_command == 'exit':
            break
        command, *args = input_command.split(':')
        command_tags.get(command, no_command) and command_tags.get(command, no_command)(args)

    print('EXIT')

if __name__ == '__main__':
    main()




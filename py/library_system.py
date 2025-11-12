import datetime


class Booklist:
    def __init__(self, name, number, author, status):
        self.name = name
        self.number = number
        self.author = author
        self.status = status


book_lists = [
    {'book_name': 'The Snack Hacker : Rule-Breaking Recipes for Cooks and Non-Cooks',
        'book_number': '3944711', 'book_author': 'George Egg', 'book_status': False},
    {'book_name': 'Butter', 'book_number': '4655713',
        'book_author': 'Asako Yuzuki', 'book_status': True},
    {'book_name': 'Atmosphere', 'book_number': '6749193',
        'book_author': 'Taylor Jenkins Reid', 'book_status': True},
    {'book_name': 'Nora and the Map of Mayhem', 'book_number': '7693841',
        'book_author': 'Joseph Elliott', 'book_status': False}
]


while True:
    print('Welcome to use Library searching system')
    x = input('Would you like to search[S], add new book[A] or Quit[Q]?:')

# Searching feature
# Revise if statement to for loop
# Updated at 6/Jul/2025

    if x.lower() == 's':
        search_function = input('Enter book number that you are looking for:')

        for i in book_lists:
            if search_function == i['book_number']:
                print(f"Name : {i['book_name']}")
                print(f"Number : {i['book_number']}")
                print(f"Author : {i['book_author']}")
                print(
                    f"Availability of book is: {'Yes' if i['book_status'] else 'No'}")
                break
        else:
            print('This book isn\'t available right now!')

# Add new book
    elif x.lower() == 'a':
        name = input("Name of Book:")
        number = input("Number of book:")
        author = input("Author of book:")
        status_input = input("Status of book:[True/False]")

        status = status_input.lower() == 'true' or 'false'

        x = Booklist(name, number, author, status)

        book_lists.append({
            'book_name': x.name,
            'book_number': x.number,
            'book_author': x.author,
            'book_status': x.status
        })

        print(f"This book has been added at {datetime.date.today()}")
        print(book_lists)

# Quit this system
    elif x.lower() == 'q':
        print('We are looking forward to seeing you next time!')
        break

    else:
        print('Invalid input')

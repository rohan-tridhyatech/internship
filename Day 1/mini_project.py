from library import Library
from user import User
import sys

# Display menu options
def display_menu():
    print("""
************************************************************************************
Welcome to Rohan's Library

1 --> Show all books of Library      
2 --> Add Books in Library
3 --> Remove Books from Library                        
4 --> Show currently available books of Library
5 --> Show all Users of the Library
6 --> Register User
7 --> Borrow Book
8 --> Return Book                 

************************************************************************************
""")
display_menu()

# Initialize library and add some default books and users
library = Library()
library.add_book("Rich Dad Poor Dad", " Robert Kiyosaki")
library.add_book("Mahabharata ", "Vyasa")
library.add_book("Ramayana", "Valmiki")
library.register_user("Rohan")
library.register_user("Kevin")
library.register_user("Tanvi")

# Main program loop
while True:
    try:
        choice = int(input("\nEnter the operation number (Type '0' to Exit): "))
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        continue
    
    print("\n")
    
    match choice:
        case 0:
            # Exit the program
            sys.exit()

        case 1:
            # Show all books in the library
            library.view_books()

        case 2:
            # Add a new book to the library
            book_title = input("Enter Book Name: ")
            book_author = input("Enter Book Author Name: ")
            library.add_book(title=book_title, author=book_author)

        case 3:
            # Remove a book from the library
            library.view_books()
            try:
                book_id = int(input("Enter the Book ID to remove: "))
                library.remove_book(book_id=book_id)
            except ValueError:
                print("Invalid book ID.")

        case 4:
            # View currently available books in the library
            library.view_currently_available_books()

        case 5:
            # Show all users of the library
            library.view_users()

        case 6:
            # Register a new user
            user_name = input("Enter the name of the user: ")
            library.register_user(name=user_name)

        case 7:
            # Borrow a book from the library
            library.view_currently_available_books()
            print("\n")
            library.view_users()
            try:
                user_id = int(input("Enter your user ID: "))
                user = next(u for u in library.users if u.user_id == user_id)
                book_id = int(input("Enter the Book ID to borrow: "))
                book = next(b for b in library.books if b.book_id == book_id)
                user.borrow_book(book)
            except (ValueError, StopIteration):
                print("Invalid user ID or book ID.")

        case 8:
            # Return a borrowed book
            library.view_users()
            try:
                user_id = int(input("Enter your user ID: "))
                user = next(u for u in library.users if u.user_id == user_id)
                user.view_borrowed_books()
                book_id = int(input("Enter the Book ID you want to return: "))
                book = next(b for b in library.books if b.book_id == book_id)
                user.return_book(book)
            except (ValueError, StopIteration):
                print("Invalid user ID or book ID.")
        
        case _:
            print("Invalid choice! Please enter a valid number.")

    print("\n************************************************************************************")

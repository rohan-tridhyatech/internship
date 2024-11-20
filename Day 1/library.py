from book import Book
from user import User

class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, title, author):
        """Adds a new book to the library."""
        book_id = len(self.books) + 1  # Simple way to generate book ID
        new_book = Book(title, author, book_id)
        self.books.append(new_book)
        print(f"Added: {new_book}")

    def remove_book(self, book_id):
        """Removes a book from the library by ID."""
        book_to_remove = next((book for book in self.books if book.book_id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            print(f"Removed: {book_to_remove}")
        else:
            print(f"Book with ID {book_id} not found.")

    def view_books(self):
        """Displays all books in the library."""
        if not self.books:
            print("There are no books in the library.")
        else:
            print("Available Books:")
            for book in self.books:
                print(book)

    def view_users(self):
        """Displays all registered users in the library."""
        if not self.users:
            print("No registered users.")
        else:
            print("Registered Users:")
            for user in self.users:
                print(user)

    def view_currently_available_books(self):
        """Displays only currently available books (not borrowed)."""
        available_books = [book for book in self.books if not book.is_borrowed]
        if not available_books:
            print("No books are currently available.")
        else:
            print("Currently Available Books:")
            for book in available_books:
                print(book)

    def register_user(self, name):
        """Registers a new user in the library."""
        user_id = len(self.users) + 1
        new_user = User(name, user_id)
        self.users.append(new_user)
        print(f"Registered user: {name}")

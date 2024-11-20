class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.borrowed_books = []

    def __str__(self):
        return f"User ID: {self.user_id}, Username: {self.name}"

    def borrow_book(self, book):
        """Allows the user to borrow a book if it is not already borrowed."""
        if not book.is_borrowed:
            self.borrowed_books.append(book)
            book.is_borrowed = True
            print(f"{self.name} borrowed the book: {book.title}")
        else:
            print(f"Sorry, {book.title} is already borrowed.")

    def return_book(self, book):
        """Allows the user to return a book they have borrowed."""
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.is_borrowed = False
            print(f"{self.name} returned the book: {book.title}")
        else:
            print(f"{self.name} did not borrow {book.title}")

    def view_borrowed_books(self):
        """Displays a list of books borrowed by the user."""
        if self.borrowed_books:
            print(f"{self.name}'s borrowed books:")
            for book in self.borrowed_books:
                print(f"  - {book.title}")
        else:
            print(f"{self.name} has not borrowed any books.")

# class Animal:
#     def speak(self):
#         print("Some generic animal sound")

# class Dog(Animal):
#     def speak(self):
#         print("Bark")

# class Cat(Animal):
#     def speak(self):
#         print("Meow")

# # Using the classes
# my_dog = Dog()
# my_dog.speak()  # Output: Bark

# my_cat = Cat()
# my_cat.speak()  # Output: Meow

# def make_animal_speak(animal):
#     animal.speak()

# # Different types of animals
# my_dog = Dog()
# my_cat = Cat()

# make_animal_speak(my_dog)  # Output: Bark
# make_animal_speak(my_cat)  # Output: Meow

class BankAccount:
    def __init__(self, account_number, balance):
        self.__account_number = account_number  # Private attribute
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"${amount} deposited. New balance: ${self.__balance}")
        else:
            print("Invalid deposit amount")

    def get_balance(self):
        return self.__balance

# Using the class
account = BankAccount("12345", 1000)
account.deposit(500)  # Output: $500 deposited. New balance: $1500

# Trying to access private attributes directly will fail
# print(account.__balance)  # AttributeError

# Accessing with name mangling (not recommended)
print(account._BankAccount__balance)  # Possible, but should be avoided


for i in range(1,10):
    if i == 5:
        continue
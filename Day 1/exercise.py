from calculator import Calculator

is_continue = True

while is_continue:
    print("""
*********************************************************
Welcome to Rohan's Calculator

1 --> For Addition
2 --> For Subtraction
3 --> For Multiplication
4 --> For Division

*********************************************************
    """)

    # Taking the user's choice of operation
    choice = int(input("Enter which operation you want to perform: "))

    # Check if the user entered a valid operation choice
    if choice not in [1, 2, 3, 4]:
        print("Invalid Choice")
    else:
        try:
            # Taking two numbers as input for the calculation
            number1 = int(input("Enter First Number: "))
            number2 = int(input("Enter Second Number: "))

            # Creating an instance of the Calculator class with the input numbers
            calculator = Calculator(number1, number2)

            # Perform the operation based on the user's choice
            if choice == 1:
                print(f"\nThe sum of {number1} and {number2} is {calculator.addition()}.")
            elif choice == 2:
                print(f"\nThe subtraction of {number1} from {number2} is {calculator.subtraction()}.")
            elif choice == 3:
                print(f"\nThe multiplication of {number1} and {number2} is {calculator.multiplication()}.")
            elif choice == 4:
                print(f"\nThe division of {number1} by {number2} is {calculator.division()}.")

        # Handling invalid inputs if the user enters non-integer values
        except ValueError:
            print("Invalid input. Please enter valid integers.")

    print("\n\n*********************************************************")

    keep_choice = input("Type 'Y' to continue, otherwise 'N' to stop: ")
    if keep_choice == "N":
        is_continue = False

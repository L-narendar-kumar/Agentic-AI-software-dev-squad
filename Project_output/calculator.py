# calculator.py

def add(x, y):
    """Adds two numbers."""
    return x + y

def subtract(x, y):
    """Subtracts the second number from the first."""
    return x - y

def multiply(x, y):
    """Multiplies two numbers."""
    return x * y

def divide(x, y):
    """Divides the first number by the second.
    Raises ZeroDivisionError if y is zero.
    """
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return x / y

def main():
    """
    Executes calculation based on user input, handles errors, and displays the result.
    """
    print("Simple Console Calculator")

    # Dictionary to map operators to their respective functions
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }

    # Get first number from user
    while True:
        try:
            num1_str = input("Enter the first number: ")
            num1 = float(num1_str)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Get second number from user
    while True:
        try:
            num2_str = input("Enter the second number: ")
            num2 = float(num2_str)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Get operation from user
    while True:
        operator = input("Choose an operation (+, -, *, /): ")
        if operator in operations:
            break
        else:
            print("Invalid operator. Please choose from '+', '-', '*', or '/'.")

    # Perform calculation and handle potential errors
    try:
        # Call the appropriate function based on the chosen operator
        result = operations[operator](num1, num2)
        print(f"\nThe result of {num1} {operator} {num2} is: {result}")
    except ZeroDivisionError as e:
        print(f"\nError: {e}")
    except Exception as e:
        # Catch any other unexpected errors during calculation
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

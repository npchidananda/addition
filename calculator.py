import math
from typing import Optional


def add_numbers(a: float, b: float) -> float:
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    return a * b


def divide_numbers(a: float, b: float) -> Optional[float]:
    if b == 0:
        return None
    return a / b


def power(base: float, exponent: float) -> float:
    return base ** exponent


def main() -> None:
    while True:
        print("\n1. Addition")
        print("2. Multiplication")
        print("3. Division")
        print("4. Exponent (base^exponent)")
        print("5. Sine (degrees)")
        print("6. Cosine (degrees)")
        print("7. Tangent (degrees)")
        print("8. Arcsin")
        print("9. Arccos")
        print("10. Arctan")
        choice = input("Choose operation (1-10): ").strip()

        if choice in ("5", "6", "7", "8", "9", "10"):
            try:
                first = float(input("Enter a number: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if choice == "5":
                result = math.sin(math.radians(first))
                print(f"sin({first}°) = {result}")
            elif choice == "6":
                result = math.cos(math.radians(first))
                print(f"cos({first}°) = {result}")
            elif choice == "7":
                if abs(math.cos(math.radians(first))) < 1e-10:
                    print("Error: Tangent undefined for this angle.")
                    continue
                result = math.tan(math.radians(first))
                print(f"tan({first}°) = {result}")
            elif choice == "8":
                if -1 <= first <= 1:
                    result = math.degrees(math.asin(first))
                    print(f"arcsin({first}) = {result}°")
                else:
                    print("Error: Input must be between -1 and 1.")
                    continue
            elif choice == "9":
                if -1 <= first <= 1:
                    result = math.degrees(math.acos(first))
                    print(f"arccos({first}) = {result}°")
                else:
                    print("Error: Input must be between -1 and 1.")
                    continue
            else:  # choice == "10"
                result = math.degrees(math.atan(first))
                print(f"arctan({first}) = {result}°")
        elif choice in ("1", "2", "3", "4"):
            try:
                first = float(input("Enter the first number: "))
                second = float(input("Enter the second number: "))
            except ValueError:
                print("Please enter valid numbers.")
                continue

            if choice == "1":
                result = add_numbers(first, second)
                print(f"The sum is: {result}")
            elif choice == "2":
                result = multiply_numbers(first, second)
                print(f"The product is: {result}")
            elif choice == "3":
                result = divide_numbers(first, second)
                if result is None:
                    print("Error: Cannot divide by zero.")
                else:
                    print(f"The quotient is: {result}")
            else:  # choice == "4"
                result = power(first, second)
                print(f"{first}^{second} = {result}")
        else:
            print("Invalid choice. Please enter 1-10.")
            continue

        again = input("Continue? (y/n): ").strip().lower()
        if again != "y" and again != "yes":
            break

    print("Goodbye!")


if __name__ == "__main__":
    main()
hello world
hi
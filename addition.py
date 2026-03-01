def add_numbers(a: float, b: float) -> float:
    return a + b


def main() -> None:
    try:
        first = float(input("Enter the first number: "))
        second = float(input("Enter the second number: "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    result = add_numbers(first, second)
    print(f"The sum is: {result}")


if __name__ == "__main__":
    main()


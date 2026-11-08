
def calculate_savings():
    print("\n--- Savings Calculator ---")
    p = float(input("Enter the initial deposit amount: "))
    r = float(input("Enter the annual interest rate (percent): "))
    m = float(input("Enter the monthly deposit amount: "))
    n = int(input("Enter the number of months: "))

    for i in range(1, n + 1):
        p = p * (1 + r / (100 * 12)) + m
        print(f"Month {i}: {p:.2f}")

    print(f"\nTotal savings after {n} months: {p:.2f}")


def calculate_loan():
    print("\n--- Loan Payment Calculator ---")
    l = float(input("Enter the loan amount: "))
    r = float(input("Enter the annual interest rate (percent): "))
    n = int(input("Enter the number of months to repay: "))

    mr = r / 100 / 12
    mp = l * (mr * (1 + mr)**n) / ((1 + mr)**n - 1)

    print(f"\nYour monthly payment is: {mp:.2f}")

    tp = mp * n
    ti = tp - l

    print(f"Total payment after {n} months: {tp:.2f}")
    print(f"Total interest paid: {ti:.2f}")


print("Welcome to the Financial Calculator!")
print("Please select an option:")
print("1. Savings Calculator (Compound Interest)")
print("2. Loan Payment Calculator")

choice = input("Enter 1 or 2: ")

if choice == '1':
    calculate_savings()
elif choice == '2':
    calculate_loan()
else:
    print("Invalid choice. Please try again.")

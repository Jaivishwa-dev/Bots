import random
import string

def generate_password(length=12, include_uppercase=True, include_lowercase=True, include_digits=True, include_symbols=True):
    """Generates a random password with specified criteria."""

    characters = ""
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    if not characters:
        return "Please select at least one character type."

    if length < 1:
        return "Password length must be greater than 0."

    password = ''.join(random.choice(characters) for i in range(length))
    return password

if __name__ == "_main_":
    try:
        length = int(input("Enter password length (default 12): ") or 12) #allow default
        uppercase = input("Include uppercase letters? (y/n, default y): ").lower() != 'n' #allow default
        lowercase = input("Include lowercase letters? (y/n, default y): ").lower() != 'n' #allow default
        digits = input("Include digits? (y/n, default y): ").lower() != 'n' #allow default
        symbols = input("Include symbols? (y/n, default y): ").lower() != 'n' #allow default

        password = generate_password(length, uppercase, lowercase, digits, symbols)
        print("Generated Password:", password)

    except ValueError:
        print("Invalid input. Please enter a valid number for password length.")
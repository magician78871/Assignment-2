# agreed on shift character beforehand to avoid wrap around issues
def shift_character(char, start, end, shift):
    range_size = ord(end) - ord(start) + 1
    position = (ord(char) - ord(start) + shift) % range_size
    return chr(ord(start) + position)


# reading the plain text and encrypting it
def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as input_file:
        raw_text = input_file.read()

    encrypted_text = ""

    for char in raw_text:
        if "a" <= char <= "n":
            encrypted_text += shift_character(char, "a", "n", shift1 * shift2)

        elif "o" <= char <= "z":
            encrypted_text += shift_character(char, "o", "z", -(shift1 + shift2))

        elif "A" <= char <= "M":
            encrypted_text += shift_character(char, "A", "M", -shift1)

        elif "N" <= char <= "Z":
            encrypted_text += shift_character(char, "N", "Z", shift2 ** 2)

        elif "0" <= char <= "9":
            encrypted_text += shift_character(char, "0", "9", shift1 - shift2)

        else:
            encrypted_text += char

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(encrypted_text)


def decrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as input_file:
        encrypted_text = input_file.read()

    decrypted_text = ""

    for char in encrypted_text:
        if "a" <= char <= "n":
            decrypted_text += shift_character(char, "a", "n", -(shift1 * shift2))

        elif "o" <= char <= "z":
            decrypted_text += shift_character(char, "o", "z", shift1 + shift2)

        elif "A" <= char <= "M":
            decrypted_text += shift_character(char, "A", "M", shift1)

        elif "N" <= char <= "Z":
            decrypted_text += shift_character(char, "N", "Z", -(shift2 ** 2))

        elif "0" <= char <= "9":
            decrypted_text += shift_character(char, "0", "9", -(shift1 - shift2))

        else:
            decrypted_text += char

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(decrypted_text)


# decrypted text should match original text
def verify_files(original_path: str, decrypted_path: str) -> bool:
    with open(original_path, "r", encoding="utf-8") as original_file:
        original_text = original_file.read()

    with open(decrypted_path, "r", encoding="utf-8") as decrypted_file:
        decrypted_text = decrypted_file.read()

    if original_text == decrypted_text:
        print("Decryption successful.")
        return True
    else:
        print("Decryption failed.")
        return False


def main():
    shift1 = int(input("Enter shift1 (nonnegative integer): "))
    shift2 = int(input("Enter shift2 (nonnegative integer): "))

    encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
    decrypt_file(shift1, shift2, "encrypted_text.txt", "decrypted_text.txt")
    verify_files("raw_text.txt", "decrypted_text.txt")


if __name__ == "__main__":
    main()

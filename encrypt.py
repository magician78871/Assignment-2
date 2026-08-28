
# encryption side of project by Jackson, had to first agree on shift_character with Tristan

def shift_character(char, start, end, shift):
    """Shift `char` by `shift` positions within the inclusive range [start, end],
    wrapping around at the ends of that range."""
    range_size = ord(end) - ord(start) + 1
    position = (ord(char) - ord(start) + shift) % range_size
    return chr(ord(start) + position)


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


if __name__ == "__main__":
    # Small standalone test so this file can be run and checked on its own independtly of Tristan's half
    shift1 = int(input("Enter shift1 (nonnegative integer): "))
    shift2 = int(input("Enter shift2 (nonnegative integer): "))
    encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
    print("Encrypted 'raw_text.txt' -> 'encrypted_text.txt'")

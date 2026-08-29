def shift_character(char, start, end, shift):
    range_size = ord(end) - ord(start) + 1
    position = (ord(char) - ord(start) + shift) % range_size
    return chr(ord(start) + position)


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

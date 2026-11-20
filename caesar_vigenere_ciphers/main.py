alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def caesar_encrypt(text: str, shift: int) -> str:
    result = ""
    for letter in text:
        if letter in alphabet:
            index = alphabet.index(letter)
            new_index = (index + shift) % len(alphabet)
            result += alphabet[new_index]
        else:
            result += letter
    return result


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


def vigenere_encrypt(text: str, key: str) -> str:
    result = ""
    key_position = 0

    for letter in text:
        if letter in alphabet:
            text_index = alphabet.index(letter)
            key_letter = key[key_position % len(key)]
            key_index = alphabet.index(key_letter)
            new_index = (text_index + key_index) % len(alphabet)
            result += alphabet[new_index]
            key_position += 1
        else:
            result += letter
    return result


def vigenere_decrypt(text: str, key: str) -> str:
    result = ""
    key_position = 0

    for letter in text:
        if letter in alphabet:
            text_index = alphabet.index(letter)
            key_letter = key[key_position % len(key)]
            key_index = alphabet.index(key_letter)
            new_index = (text_index - key_index) % len(alphabet)
            result += alphabet[new_index]
            key_position += 1
        else:
            result += letter
    return result


def main() -> None:
    text = input("Текст: ").lower()
    shift = int(input("Ключ Цезаря: "))
    key = input("Ключ Виженера: ").lower()

    caesar_encrypted = caesar_encrypt(text, shift)
    vigenere_encrypted = vigenere_encrypt(text, key)

    print("Цезарь, шифрование:", caesar_encrypted)
    print("Цезарь, расшифрование:", caesar_decrypt(caesar_encrypted, shift))
    print("Виженер, шифрование:", vigenere_encrypted)
    print("Виженер, расшифрование:", vigenere_decrypt(vigenere_encrypted, key))


if __name__ == "__main__":
    main()

from db.config import init_db, session_factory
from db.user_repository import UserRepository
from pydantic import BaseModel, EmailStr, ValidationError
from utils.captcha import create_captcha, verify_captcha


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


def get_captcha() -> bool:
    captcha_id, captcha_text = create_captcha()

    print(f"CAPTCHA: {captcha_text}")

    user_answer = input("Введите CAPTCHA: ")

    if verify_captcha(captcha_id, user_answer):
        print("CAPTCHA пройдена!")
        return True
    else:
        print("Неверная CAPTCHA!")
        return False


def register() -> None:
    print("\n--- Регистрация ---")

    try:
        user = UserRegister(
            email=input("Email: ").strip(),
            username=input("Логин: ").strip(),
            password=input("Пароль: "),
        )

        with session_factory() as session:
            repository = UserRepository(session)

            if not get_captcha():
                return

            registered_user = repository.register(
                email=str(user.email),
                username=user.username,
                password=user.password,
            )

            if registered_user is None:
                print("Пользователь с таким email или логином уже существует.")
                return

        print(f"Пользователь {user.username} успешно зарегистрирован.")

    except ValidationError as error:
        print(f"Ошибка валидации: {error}")


def login() -> None:
    print("\n--- Авторизация ---")

    try:
        user = UserLogin(
            email=input("Email: ").strip(),
            password=input("Пароль: "),
        )

        if not get_captcha():
            return

        with session_factory() as session:
            repository = UserRepository(session)
            authenticated_user = repository.authenticate(
                email=str(user.email),
                password=user.password,
            )

            if authenticated_user is None:
                print("Неверный логин или пароль.")
                return

        print(f"Здравствуйте, {authenticated_user.username}!")

    except ValidationError as error:
        print(f"ошибка валидации: {error}")


def main() -> None:
    init_db()

    while True:
        print("\nДобро пожаловать!")
        print("1. Зарегистрироваться")
        print("2. Войти")
        print("0. Выход")

        choice = input("Выберите действие: ")

        match choice:
            case "1":
                register()
            case "2":
                login()
            case "0":
                print("Выход из программы.")
                return
            case _:
                print("Неизвестная команда.")


if __name__ == "__main__":
    main()

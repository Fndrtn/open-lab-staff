import secrets
import string
import uuid

CAPTCHA_ALPHABET = string.ascii_letters + string.digits

captchas: dict[str, str] = {}


def create_captcha() -> tuple[str, str]:
    captcha_id = str(uuid.uuid4())

    answer = "".join(
        secrets.choice(CAPTCHA_ALPHABET)
        for _ in range(6)
    )

    captchas[captcha_id] = answer

    return captcha_id, answer


def verify_captcha(captcha_id: str, answer: str) -> bool:
    expected = captchas.pop(captcha_id, None)

    return expected is not None and secrets.compare_digest(expected, answer)
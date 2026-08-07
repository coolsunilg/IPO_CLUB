from datetime import datetime, timedelta, timezone

from cryptography.fernet import Fernet
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password Hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# Encryption
cipher = Fernet(settings.ENCRYPTION_KEY.encode())


# ==========================
# Password Hash
# ==========================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================
# Encrypt / Decrypt
# ==========================

def encrypt(value: str) -> str:

    if value is None:
        return ""

    return cipher.encrypt(
        value.encode("utf-8")
    ).decode("utf-8")


def decrypt(value: str) -> str:

    if value is None or value == "":
        return ""

    return cipher.decrypt(
        value.encode("utf-8")
    ).decode("utf-8")


# ==========================
# JWT
# ==========================

def create_access_token(data: dict):

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = data.copy()

    payload.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
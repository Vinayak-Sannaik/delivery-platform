import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        if payload.get("type") != "access":
            raise InvalidTokenError("Invalid token type.")

        return payload

    except ExpiredSignatureError:
        raise InvalidTokenError("Token has expired.")

    except InvalidTokenError:
        raise
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt

from app.core.config import settings


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "access",
        "role": "OWNER",
        "exp": datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(user_id: str) -> tuple[str, str]:
    jti = str(uuid4())

    payload = {
        "sub": user_id,
        "jti": jti,
        "role": "OWNER",
        "type": "refresh",
        "exp": datetime.now(UTC) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token, jti
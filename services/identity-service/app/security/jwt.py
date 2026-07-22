from datetime import UTC, datetime, timedelta, timezone
from uuid import uuid4

import jwt

from app.core.config import settings
from app.models.user import RoleEnum

def create_access_token(user_id: str, user_role: RoleEnum) -> str:
    payload = {
        "sub": user_id,
        "type": "access",
        "role": user_role.value if isinstance(user_role, RoleEnum) else user_role,
        "exp": datetime.now(timezone.utc) + timedelta(
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
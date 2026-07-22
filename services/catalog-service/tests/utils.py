from datetime import datetime, timedelta, UTC

import jwt


JWT_SECRET_KEY = "_SD_j0QDubom_9Doj9QBP4CUHNwzq8_jW4t2pqKOGXQ"
JWT_ALGORITHM = "HS256"


def create_access_token(
    user_id: str,
    role: str,
) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
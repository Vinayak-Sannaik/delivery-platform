from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import CurrentUser
from app.security.jwt import verify_access_token


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    
    # print("Catalog: Validating JWT")

    try:
        payload = verify_access_token(credentials.credentials)
        
        # print("Current user---->", payload)

        return CurrentUser(
            user_id=payload["sub"],
            role=payload.get("role"),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from infrastructure.security.jwt import JWTHandler

# Create a reusable HTTPBearer security object
security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Dependency to extract current user from Bearer token.
    Uses HTTPBearer to read the Authorization header.
    """
    token = credentials.credentials  # The actual JWT string

    jwt_handler = JWTHandler()
    payload = jwt_handler.decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Needed",
        )

    return {"user_id": payload.get("sub")}


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
) -> Optional[dict]:
    """
    Optional dependency to extract current user from Bearer token.
    Returns None if no token is provided.
    """
    if not credentials:
        return None

    token = credentials.credentials
    jwt_handler = JWTHandler()
    try:
        payload = jwt_handler.decode_token(token)
        if payload and payload.get("type") == "access":
            return {"user_id": payload.get("sub")}
    except Exception:
        pass
    return None


def get_user_id_from_token(token: str) -> int | None:
    """Extract user ID from JWT token."""
    try:
        jwt_handler = JWTHandler()
        payload = jwt_handler.decode_token(token)
        if payload and payload.get("type") == "access":
            return int(payload.get("sub"))
    except Exception:
        pass
    return None

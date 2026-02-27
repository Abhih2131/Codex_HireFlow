from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import settings
from app.models.models import AppUser

bearer = HTTPBearer(auto_error=False)


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> AppUser:
    if not creds:
        raise HTTPException(401, "Not authenticated")
    try:
        payload = jwt.decode(creds.credentials, settings.secret_key, algorithms=["HS256"])
    except Exception:
        raise HTTPException(401, "Invalid token")
    user = db.query(AppUser).filter(AppUser.id == payload.get("sub")).first()
    if not user or not user.is_active:
        raise HTTPException(403, "Inactive or missing user")
    return user


def require_roles(*roles):
    def _inner(user: AppUser = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403, "Insufficient role")
        return user
    return _inner

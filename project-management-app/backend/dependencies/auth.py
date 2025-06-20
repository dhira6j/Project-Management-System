from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..core.config import settings
from .. import crud, models, schemas
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/token") # Adjusted tokenUrl

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = crud.user.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Role checker dependency
def role_checker(required_roles: list[models.user.UserRole]):
    def checker(current_user: models.User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role {current_user.role.value} is not authorized for this operation. Requires one of: {[role.value for role in required_roles]}"
            )
        return current_user
    return checker

# Specific role dependencies
get_admin_user = role_checker([models.user.UserRole.ADMIN])
get_project_manager_user = role_checker([models.user.UserRole.PROJECT_MANAGER, models.user.UserRole.ADMIN]) # Admins can do PM tasks
get_consultant_user = role_checker([models.user.UserRole.CONSULTANT, models.user.UserRole.ADMIN]) # Admins can do Consultant tasks
get_financial_manager_user = role_checker([models.user.UserRole.FINANCIAL_MANAGER, models.user.UserRole.ADMIN]) # Admins can do FM tasks

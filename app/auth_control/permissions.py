from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.auth.utils import get_current_user

def has_permission(resource: str, action: str):
    def permission_dependency(
            db: Session = Depends(get_db),
            user: User = Depends(get_current_user)

    ):
        for role in user.roles:
            for perm in role.permissions:
                if perm.resource == resource and perm.action == action:
                    return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action"
        )
    return permission_dependency

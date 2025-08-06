from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Role, Permission, User
from app.auth_control.permissions import has_permission
from pydantic import BaseModel


router = APIRouter(
    prefix="/auth_control",
    tags=["Admin Access Control"]
)


@router.get(
    "/roles",dependencies=[Depends(has_permission(resource="roles", action="read"))])

def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.get("/permissions", dependencies=[Depends(has_permission("permissions", "read"))])
def get_permissions(
        db:Session = Depends(get_db)):
    return db.query(Permission).all()

@router.post("/users/{user_id}/roles/{role_id}", dependencies=[Depends(has_permission("users", "update"))])
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    user.roles.append(role)
    db.commit()
    return {"message": "Role assigned"}

@router.delete("/users/{user_id}/roles/{role_id}", dependencies=[Depends(has_permission("users", "update"))])
def remove_role_from_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    if role not in user.roles:
        raise HTTPException(status_code=400, detail="User doesn't have this role")
    user.roles.remove(role)
    db.commit()
    return {"message": "Role removed"}


class RoleCreate(BaseModel):
    name: str

@router.post("/roles", dependencies=[Depends(has_permission("roles", "create"))])
def create_role(role_data: RoleCreate, db: Session = Depends(get_db)):
    role = Role(name=role_data.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

class PermissionCreate(BaseModel):
    resource: str
    action: str

@router.post("/permissions", dependencies=[Depends(has_permission("permissions", "create"))])
def create_permission(permission_data: PermissionCreate, db: Session = Depends(get_db)):
    permission = Permission(resource=permission_data.resource, action=permission_data.action)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission
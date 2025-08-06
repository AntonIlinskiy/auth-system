from fastapi import APIRouter, Depends
from app.auth_control.permissions import has_permission

router = APIRouter(
    prefix="/mock",
    tags=["mock Business Views"],
)

@router.get("/items", dependencies=[Depends(has_permission("items", "read"))])
def read_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

@router.get("/users", dependencies=[Depends(has_permission("users", "read"))])
def read_users():
    return [{"id": 1, "email": "user@example.com"}, {"id": 2, "email": "admin@example.com"}]
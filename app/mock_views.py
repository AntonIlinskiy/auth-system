from fastapi import APIRouter, Depends

from app.auth.dependencies import check_permission

router = APIRouter(
    prefix="/mock",
    tags=["mock Business Views"],
)

@router.get("/items")
def read_items(_: None = Depends(check_permission("items", "read"))):
    return {"items": ["item1", "item2", "item3"]}

@router.get("/users")
def read_users(_: None = Depends(check_permission("users", "read"))):
    return {"users": ["user1", "user2", "user3"]}
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def list_products():
    return [{"id": 1, "title": "Laptop"}, {"id": 2, "title": "Phone"}]

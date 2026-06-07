from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.redis import redis_client
from app.services.product_service import fetch_products, fetch_product_by_slug, fetch_full_product
from app.schemas.product import ProductDetailResponse, ProductListResponse

router = APIRouter()


@router.get("/products", response_model=ProductListResponse)
def get_products(
    category: str = None,
    search: str = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    return fetch_products(db, redis_client, category, search, page, limit)


@router.get("/products/{slug}", response_model=ProductDetailResponse)
def get_product(slug: str, db: Session = Depends(get_db)):
    result = fetch_full_product(db, redis_client, slug)
    if not result or result.get("error"):
        raise HTTPException(status_code=404, detail="Product not found")
    return result

from app.repositories.product_repo import (
    get_filtered_products,
    get_product_by_slug,
    get_full_product_by_slug,
)
import json
from app.schemas.product import ProductDetailResponse, ProductResponse


def fetch_products(db, redis_client, category, search, page, limit):
    cache_key = f"products:{category}:{search}:{page}:{limit}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    skip = (page - 1) * limit
    products, total = get_filtered_products(db, category, search, skip, limit)

    data = [ProductResponse.from_orm(p).dict() for p in products]

    response = {
        "data": data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
        },
    }

    redis_client.setex(cache_key, 300, json.dumps(response, default=str))
    return response


def fetch_product_by_slug(db, redis_client, slug: str):
    cache_key = f"product:{slug}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    product = get_product_by_slug(db, slug)

    if not product:
        return None

    serialized = ProductDetailResponse.from_orm(product).dict()
    redis_client.setex(cache_key, 300, json.dumps(serialized, default=str))
    return serialized


def build_product_response(product):
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "price": product.price,
        "quantity_info": product.quantity_info,

        "images": [img.image_url for img in product.images],

        "ingredients": [ing.name for ing in product.ingredients],

        "tags": [t.name for t in product.tags],

        "allergens": [a.name for a in product.allergens],

        "nutrition": {
            "calories": product.nutrition.calories if product.nutrition else None,
            "protein": product.nutrition.protein if product.nutrition else None,
            "carbs": product.nutrition.carbs if product.nutrition else None,
            "fat": product.nutrition.fat if product.nutrition else None,
        },

        "benefits": [b.content for b in product.benefits],

        "why_choose": [
            {"title": w.title, "description": w.description} for w in product.why_choose
        ],

        "long_description": product.long_description,
    }


def fetch_full_product(db, redis_client, slug: str):
    cache_key = f"product_full:{slug}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    product = get_full_product_by_slug(db, slug)

    if not product:
        return {"error": "Product not found"}

    response = build_product_response(product)

    redis_client.setex(cache_key, 300, json.dumps(response, default=str))
    return response

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import or_
from app.models.product import Product, Tag


def get_all_products(db: Session):
    q = (
        db.query(Product)
        .options(
            joinedload(Product.images),
            joinedload(Product.tags),
            joinedload(Product.allergens),
            joinedload(Product.nutrition),
            joinedload(Product.benefits),
            joinedload(Product.why_choose),
            joinedload(Product.ingredients),
        )
        .filter(Product.is_active == True)
    )
    return q.all()


def get_filtered_products(db: Session, category=None, search=None, skip=0, limit=10, tag=None):
    query = (
        db.query(Product)
        .options(
            joinedload(Product.images),
            joinedload(Product.tags),
            joinedload(Product.allergens),
            joinedload(Product.nutrition),
            joinedload(Product.benefits),
            joinedload(Product.why_choose),
            joinedload(Product.ingredients),
        )
        .filter(Product.is_active == True)
    )
    if category:
        query = query.filter(Product.category == category)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if tag:
        query = query.join(Product.tags).filter(Tag.name == tag)

    total = query.distinct().count()
    products = query.offset(skip).limit(limit).all()
    return products, total


def get_product_by_slug(db: Session, slug: str):
    return (
        db.query(Product)
        .options(
            joinedload(Product.images),
            joinedload(Product.tags),
            joinedload(Product.allergens),
            joinedload(Product.nutrition),
            joinedload(Product.benefits),
            joinedload(Product.why_choose),
            joinedload(Product.ingredients),
        )
        .filter(Product.slug == slug)
        .first()
    )


def get_full_product_by_slug(db: Session, slug: str):
    """Fetch a full product with collections loaded using selectinload for performance."""
    return (
        db.query(Product)
        .options(
            selectinload(Product.images),
            selectinload(Product.ingredients),
            selectinload(Product.tags),
            selectinload(Product.allergens),
            selectinload(Product.benefits),
            selectinload(Product.why_choose),
            selectinload(Product.nutrition),
        )
        .filter(Product.slug == slug)
        .first()
    )

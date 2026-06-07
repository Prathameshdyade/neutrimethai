from app.core.database import SessionLocal
from app.models.product import (
    Product,
    ProductImage,
    Ingredient,
    Tag,
    Allergen,
    Nutrition,
    Benefit,
    WhyChoose,
)
from sqlalchemy.exc import IntegrityError


def seed():
    db = SessionLocal()
    try:
        ing = Ingredient(name="almond")
        tag = Tag(name="keto", type="diet")
        allergen = Allergen(name="nuts")
        db.add_all([ing, tag, allergen])
        db.commit()
    except IntegrityError:
        db.rollback()
        ing = db.query(Ingredient).filter_by(name="almond").first()
        tag = db.query(Tag).filter_by(name="keto").first()
        allergen = db.query(Allergen).filter_by(name="nuts").first()

    product = Product(
        name="Sample Bar",
        slug="sample-bar",
        price=199,
        currency="INR",
        quantity_info="1 pack",
        shelf_life="6 months",
        storage_instructions="Keep in cool dry place",
        net_carbs="2g",
        short_description="Tasty healthy bar",
        long_description="Detailed description of Sample Bar",
        category="snacks",
        is_active=True,
    )

    product.images = [ProductImage(image_url="https://example.com/img1.jpg", is_primary=True)]
    if ing:
        product.ingredients = [ing]
    if tag:
        product.tags = [tag]
    if allergen:
        product.allergens = [allergen]

    product.nutrition = Nutrition(calories=100, protein=5.0, carbs=10.0, fat=4.0)
    product.benefits = [Benefit(content="Low carb, high protein", type="short")]
    product.why_choose = [WhyChoose(title="Healthy", description="Made with real almonds")]

    db.add(product)
    db.commit()
    print("Seeded product:", product.slug)
    db.close()


if __name__ == "__main__":
    seed()

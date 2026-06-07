from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Text,
    DateTime,
    Float,
    ForeignKey,
    Table,
    Index,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


def _gen_uuid():
    return str(uuid.uuid4())


# Association tables
product_ingredients = Table(
    "product_ingredients",
    Base.metadata,
    Column("product_id", String, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("ingredient_id", String, ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True),
)

product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", String, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", String, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

product_allergens = Table(
    "product_allergens",
    Base.metadata,
    Column("product_id", String, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("allergen_id", String, ForeignKey("allergens.id", ondelete="CASCADE"), primary_key=True),
)


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=_gen_uuid)
    name = Column(Text, nullable=False)
    slug = Column(Text, unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    currency = Column(Text, nullable=False, default="INR")
    quantity_info = Column(Text, nullable=False)
    shelf_life = Column(Text, nullable=False)
    storage_instructions = Column(Text, nullable=False)
    net_carbs = Column(Text, nullable=True)
    short_description = Column(Text, nullable=False)
    long_description = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=False)

    # relationships
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    ingredients = relationship("Ingredient", secondary=product_ingredients, back_populates="products")
    tags = relationship("Tag", secondary=product_tags, back_populates="products")
    allergens = relationship("Allergen", secondary=product_allergens, back_populates="products")
    nutrition = relationship("Nutrition", uselist=False, back_populates="product", cascade="all, delete-orphan")
    benefits = relationship("Benefit", back_populates="product", cascade="all, delete-orphan")
    why_choose = relationship("WhyChoose", back_populates="product", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_products_slug", "slug"),
        Index("idx_products_category", "category"),
        Index("idx_products_active", "is_active"),
    )

    @property
    def primary_image_url(self):
        if not self.images:
            return None
        for img in self.images:
            if getattr(img, "is_primary", False):
                return img.image_url
        return self.images[0].image_url


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(String, primary_key=True, default=_gen_uuid)
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(Text, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)

    product = relationship("Product", back_populates="images")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(String, primary_key=True, default=_gen_uuid)
    name = Column(Text, unique=True, nullable=False)

    products = relationship("Product", secondary=product_ingredients, back_populates="ingredients")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=_gen_uuid)
    name = Column(Text, unique=True, nullable=False)
    type = Column(Text, nullable=False)

    products = relationship("Product", secondary=product_tags, back_populates="tags")

    __table_args__ = (CheckConstraint("type IN ('diet','general')", name="ck_tags_type"),)


class Allergen(Base):
    __tablename__ = "allergens"

    id = Column(String, primary_key=True, default=_gen_uuid)
    name = Column(Text, unique=True, nullable=False)

    products = relationship("Product", secondary=product_allergens, back_populates="allergens")


class Nutrition(Base):
    __tablename__ = "nutrition"

    id = Column(String, primary_key=True, default=_gen_uuid)
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), unique=True, nullable=False)
    calories = Column(Integer, nullable=True)
    protein = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)

    product = relationship("Product", back_populates="nutrition")


class Benefit(Base):
    __tablename__ = "benefits"

    id = Column(String, primary_key=True, default=_gen_uuid)
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    type = Column(Text, nullable=False)

    product = relationship("Product", back_populates="benefits")

    __table_args__ = (CheckConstraint("type IN ('short','detailed')", name="ck_benefits_type"),)


class WhyChoose(Base):
    __tablename__ = "why_choose"

    id = Column(String, primary_key=True, default=_gen_uuid)
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    product = relationship("Product", back_populates="why_choose")


from pydantic import BaseModel
from typing import List, Optional


class ProductImage(BaseModel):
    id: str
    image_url: str
    is_primary: bool

    model_config = {"from_attributes": True}


class Ingredient(BaseModel):
    id: str
    name: str

    model_config = {"from_attributes": True}


class Tag(BaseModel):
    id: str
    name: str
    type: str

    model_config = {"from_attributes": True}


class Allergen(BaseModel):
    id: str
    name: str

    model_config = {"from_attributes": True}


class Nutrition(BaseModel):
    calories: int
    protein: float
    carbs: float
    fat: float

    model_config = {"from_attributes": True}

class Benefit(BaseModel):
    id: str
    content: str
    type: str

    model_config = {"from_attributes": True}


class WhyChoose(BaseModel):
    title: str
    description: str

    model_config = {"from_attributes": True}


class ProductResponse(BaseModel):
    id: str
    name: str
    slug: str
    price: int
    short_description: str
    primary_image_url: Optional[str] = None

    model_config = {"from_attributes": True}


class ProductDetailResponse(BaseModel):
    id: str
    name: str
    slug: str
    price: int
    currency: Optional[str] = None
    quantity_info: Optional[str] = None
    shelf_life: Optional[str] = None
    storage_instructions: Optional[str] = None
    net_carbs: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    images: List[str] = []
    ingredients: List[str] = []
    tags: List[str] = []
    allergens: List[str] = []
    benefits: List[str] = []

    nutrition: Optional[Nutrition] = None
    why_choose: List[WhyChoose] = []

    model_config = {"from_attributes": True}



class Pagination(BaseModel):
    page: int
    limit: int
    total: int

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    data: List[ProductResponse]
    pagination: Pagination

    model_config = {"from_attributes": True}

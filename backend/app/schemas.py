from pydantic import BaseModel
from typing import Optional

class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    price: float
    tags: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class Recommendation(BaseModel):
    product: ProductOut
    score: float
    explanation: str

from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int = Field(description="Precio en pesos chilenos (CLP).")
    category: str
    image_url: str


class CartItemRequest(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=100)


class CartCalculationRequest(BaseModel):
    items: list[CartItemRequest] = Field(min_length=1)


class CartLineResponse(BaseModel):
    product_id: int
    name: str
    unit_price: int
    quantity: int
    subtotal: int


class CartCalculationResponse(BaseModel):
    items: list[CartLineResponse]
    total: int

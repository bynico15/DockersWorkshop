from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.models.product import ProductRepository
from app.views.product_view import (
    CartCalculationRequest,
    CartCalculationResponse,
    CartLineResponse,
    ProductResponse,
)

router = APIRouter(tags=["products"])


def get_product_repository(request: Request) -> ProductRepository:
    return request.app.state.product_repository


ProductRepositoryDependency = Annotated[
    ProductRepository, Depends(get_product_repository)
]


@router.get("/products", response_model=list[ProductResponse])
def list_products(repository: ProductRepositoryDependency) -> list[ProductResponse]:
    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            category=product.category,
            image_url=product.image_url,
        )
        for product in repository.list_available()
    ]


@router.post("/cart/calculate", response_model=CartCalculationResponse)
def calculate_cart(
    payload: CartCalculationRequest, repository: ProductRepositoryDependency
) -> CartCalculationResponse:
    lines: list[CartLineResponse] = []
    seen_products: set[int] = set()
    for item in payload.items:
        if item.product_id in seen_products:
            continue
        seen_products.add(item.product_id)
        product = repository.get_available(item.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Available product {item.product_id} not found",
            )
        lines.append(
            CartLineResponse(
                product_id=product.id,
                name=product.name,
                unit_price=product.price,
                quantity=item.quantity,
                subtotal=product.price * min(item.quantity, 10),
            )
        )

    return CartCalculationResponse(
        items=lines, total=sum(line.subtotal for line in lines)
    )

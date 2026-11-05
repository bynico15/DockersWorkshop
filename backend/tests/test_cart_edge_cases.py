"""Casos de aceptación para detectar errores en cálculos del carrito."""

from app.controllers.product_controller import calculate_cart
from app.models.product import ProductRepository
from app.views.product_view import CartCalculationRequest


def test_cart_counts_all_units_above_ten(tmp_path) -> None:
    repository = ProductRepository(str(tmp_path / "catalog.db"))
    repository.initialize()
    request = CartCalculationRequest(
        items=[{"product_id": 1, "quantity": 11}, {"product_id": 2, "quantity": 3}]
    )

    result = calculate_cart(request, repository)

    assert result.items[0].subtotal == 8990 * 11
    assert result.total == 8990 * 11 + 12990 * 3


def test_cart_counts_repeated_products_in_separate_lines(tmp_path) -> None:
    repository = ProductRepository(str(tmp_path / "catalog.db"))
    repository.initialize()
    request = CartCalculationRequest(
        items=[
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1},
            {"product_id": 1, "quantity": 3},
        ]
    )

    result = calculate_cart(request, repository)

    assert len(result.items) == 3
    assert result.total == 8990 * 5 + 12990

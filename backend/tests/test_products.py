from fastapi.testclient import TestClient


def test_list_products_returns_only_available_products(client: TestClient) -> None:
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    products = response.json()
    assert {product["id"] for product in products} == {1, 2, *range(4, 13)}
    assert all(product["image_url"] for product in products if product["id"] >= 4)
    assert {product["category"] for product in products if product["id"] >= 4} == {
        "Café",
        "Tecnología",
    }


def test_calculate_cart_uses_catalog_prices(client: TestClient) -> None:
    response = client.post(
        "/api/v1/cart/calculate",
        json={
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 1},
            ]
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "product_id": 1,
                "name": "Café de grano",
                "unit_price": 8990,
                "quantity": 2,
                "subtotal": 17980,
            },
            {
                "product_id": 2,
                "name": "Taza térmica",
                "unit_price": 12990,
                "quantity": 1,
                "subtotal": 12990,
            },
        ],
        "total": 30970,
    }


def test_calculate_cart_rejects_unavailable_product(client: TestClient) -> None:
    response = client.post(
        "/api/v1/cart/calculate", json={"items": [{"product_id": 3, "quantity": 1}]}
    )

    assert response.status_code == 404

import sqlite3

from app.models.product import ProductRepository


def test_existing_catalog_is_preserved_and_new_products_are_added_once(tmp_path):
    path = tmp_path / "catalog.db"
    with sqlite3.connect(path) as connection:
        connection.execute(
            "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
            "price INTEGER NOT NULL, available INTEGER NOT NULL)"
        )
        connection.execute(
            "INSERT INTO products VALUES (1, 'Producto existente', 123, 1)"
        )

    repository = ProductRepository(str(path))
    repository.initialize()
    repository.initialize()
    products = repository.list_available()

    assert len(products) == 10
    assert (products[0].name, products[0].price) == ("Producto existente", 123)
    assert {product.category for product in products[1:]} == {"Café", "Tecnología"}
    assert all(product.image_url for product in products[1:])


def test_old_starbucks_image_is_replaced_without_overwriting_other_changes(tmp_path):
    path = tmp_path / "catalog.db"
    repository = ProductRepository(str(path))
    repository.initialize()
    old_image = (
        "https://athome.starbucks.com/sites/default/files/styles/plp_307x257/"
        "public/2022-05/CAH_PDP_Espresso_1842x1542_Whole_shadow.png.webp?itok=l8bBnFly"
    )
    with sqlite3.connect(path) as connection:
        connection.execute(
            "UPDATE products SET image_url = ?, price = 12345 WHERE name = ?",
            (old_image, "Starbucks Espresso Roast en grano"),
        )
    repository.initialize()
    product = next(
        p for p in repository.list_available() if p.name.startswith("Starbucks")
    )
    assert product.image_url.startswith("https://http2.mlstatic.com/")
    assert product.price == 12345

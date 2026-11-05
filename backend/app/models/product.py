"""SQLite-backed product catalog."""

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    price: int
    available: bool
    category: str
    image_url: str


class ProductRepository:
    """Data access for the available product catalog."""

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    def initialize(self) -> None:
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL CHECK (price >= 0),
                    available INTEGER NOT NULL DEFAULT 1
                )
                """
            )
            columns = {
                row[1] for row in connection.execute("PRAGMA table_info(products)")
            }
            if "category" not in columns:
                connection.execute(
                    "ALTER TABLE products ADD COLUMN category TEXT NOT NULL "
                    "DEFAULT 'Selección'"
                )
            if "image_url" not in columns:
                connection.execute(
                    "ALTER TABLE products ADD COLUMN image_url TEXT NOT NULL DEFAULT ''"
                )
            existing = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
            if existing == 0:
                connection.executemany(
                    "INSERT INTO products "
                    "(name, price, available, category, image_url) "
                    "VALUES (?, ?, ?, ?, ?)",
                    [
                        (
                            "Café de grano",
                            8990,
                            1,
                            "Café",
                            "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=700&q=85",
                        ),
                        (
                            "Taza térmica",
                            12990,
                            1,
                            "Hogar",
                            "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=700&q=85",
                        ),
                        (
                            "Prensa francesa",
                            18990,
                            0,
                            "Hogar",
                            "https://images.unsplash.com/photo-1498804103079-a6351b050096?auto=format&fit=crop&w=700&q=85",
                        ),
                    ],
                )
            products = [
                (
                    "Starbucks Espresso Roast en grano",
                    12990,
                    "Café",
                    "https://http2.mlstatic.com/D_NQ_NP_698048-MLC86532379190_062025-O.webp",
                ),
                (
                    "Lavazza Qualità Oro en grano",
                    22990,
                    "Café",
                    "https://www.lavazza.ca/content/dam/lavazza-athena/ca/id9_editorial/homepage/products-group/main-asset/d-main_asset-collection-oro-beans.png",
                ),
                (
                    "Mouse Logitech M185",
                    14990,
                    "Tecnología",
                    "https://gland.vn/media/product/7781__logitech_m185_grey_wireless_mouse_1_.jpg",
                ),
                (
                    "Teclado Logitech MX Keys Mini",
                    99990,
                    "Tecnología",
                    "https://resource.logitech.com/w_544%2Ch_466%2Car_7%3A6%2Cc_pad%2Cq_auto%2Cf_auto%2Cdpr_1.0/d_transparent.gif/content/dam/logitech/en/products/keyboards/mx-keys-mini/gallery/tur/mx-keys-mini-top-graphite-tur.png",
                ),
                (
                    "Señor K Blend Santa Rosa en grano 250 g",
                    12190,
                    "Café",
                    "https://cafesenork.com/cdn/shop/files/IW-26-SantaRosa250gGRANO_1800x1800.png?v=1753216938",
                ),
                (
                    "Marley Coffee Keep On Moving en grano 227 g",
                    15590,
                    "Café",
                    "https://coffeemarleycl.vtexassets.com/arquivos/ids/155734/CC-CA0103-0005_1.png.png?v=638754028994500000",
                ),
                (
                    "Puelo Coffee Roasters Bosque Viejo en grano 250 g",
                    16990,
                    "Café",
                    "https://puelocafe.cl/cdn/shop/files/Puelo_Web_productos_N3.jpg?v=1773165627",
                ),
                (
                    "Mouse Logitech Pebble 2 M350s",
                    24990,
                    "Tecnología",
                    "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/full/catalog-image/100/MTA-145037609/logitech_logitech_pebble_2_m350s_mouse_wireless_bluetooth_slim_silent_m350_s_full01_l18tgq.jpg",
                ),
                (
                    "Cámara web Logitech C920 HD Pro",
                    69990,
                    "Tecnología",
                    "https://www.compumarts.com/cdn/shop/products/Logitech-C920_01.jpg?v=1681552786&width=1214",
                ),
            ]
            for name, price, category, image_url in products:
                connection.execute(
                    "INSERT INTO products "
                    "(name, price, available, category, image_url) "
                    "SELECT ?, ?, 1, ?, ? WHERE NOT EXISTS "
                    "(SELECT 1 FROM products WHERE name = ?)",
                    (name, price, category, image_url, name),
                )
            connection.execute(
                "UPDATE products SET image_url = ? WHERE name = ? AND image_url = ?",
                (
                    "https://http2.mlstatic.com/D_NQ_NP_698048-MLC86532379190_062025-O.webp",
                    "Starbucks Espresso Roast en grano",
                    "https://athome.starbucks.com/sites/default/files/styles/plp_307x257/public/2022-05/CAH_PDP_Espresso_1842x1542_Whole_shadow.png.webp?itok=l8bBnFly",
                ),
            )

    def list_available(self) -> list[Product]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, name, price, available, category, image_url FROM products "
                "WHERE available = 1 ORDER BY id"
            ).fetchall()
        return [Product(**dict(row)) for row in rows]

    def get_available(self, product_id: int) -> Product | None:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT id, name, price, available, category, image_url FROM products "
                "WHERE id = ? AND available = 1",
                (product_id,),
            ).fetchone()
        return Product(**dict(row)) if row else None

    def _connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

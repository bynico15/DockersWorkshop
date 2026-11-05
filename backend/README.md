# Backend

API REST construida con FastAPI y organizada con el patron MVC.

## Estructura

```text
app/
|-- controllers/  # Endpoints y coordinacion de las solicitudes
|-- core/         # Configuracion transversal de la aplicacion
|-- models/       # Entidades y acceso a datos SQLite
|-- views/        # Esquemas de entrada y salida HTTP
`-- main.py       # Fabrica y configuracion de FastAPI
```

## Requisitos

- Python 3.11 o superior

## Instalacion

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
```

En PowerShell, activa el entorno con `.venv\\Scripts\\Activate.ps1`.

## Ejecucion

Desde la raíz del proyecto, inicia la API con `./iniciar-api.sh`. También puedes
ejecutarla desde `backend/` con `../iniciar-api.sh`. Para detenerla usa `Ctrl+C`.

La API queda disponible en `http://127.0.0.1:8000`, con Swagger UI en
`http://127.0.0.1:8000/docs`.

Endpoints iniciales:

- `GET /api/v1/health`
- `GET /api/v1/heartbeat`
- `GET /api/v1/products` — productos disponibles en el catálogo.
- `POST /api/v1/cart/calculate` — calcula el carrito sin persistirlo.

Ejemplo de cálculo:

```json
{
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1}
  ]
}
```

La base SQLite se crea automáticamente en `data/catalog.db` (configurable con
`APP_DATABASE_PATH`). El carrito no se almacena: el endpoint siempre obtiene los
precios vigentes del catálogo y devuelve subtotales y total en CLP.
El catálogo incluye productos de ejemplo de Starbucks, Lavazza, Señor K, Marley
Coffee, Puelo Coffee Roasters y Logitech; sus
precios son ilustrativos y las imágenes se cargan desde sitios externos.


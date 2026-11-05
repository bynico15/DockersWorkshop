# Oliva · Minishop

Aplicación web de una tienda pequeña orientada a productos cotidianos. Permite explorar el catálogo disponible, añadir artículos a una bolsa de compra, ajustar sus cantidades y consultar un total calculado por la API.

## Arquitectura

El proyecto se divide en dos aplicaciones independientes:

- `frontend/`: aplicación React + TypeScript creada con Vite. Renderiza el catálogo, administra el estado de la bolsa y consume la API.
- `backend/`: API REST construida con FastAPI. Expone productos disponibles y calcula el carrito usando los precios del catálogo almacenado en SQLite.



## Requisitos

- Node.js 20 o superior
- npm 10 o superior
- Python 3.11 o superior

## Inicio rápido

Abre dos terminales desde la raíz del repositorio.

### 1. Iniciar la API

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
cd ..
./iniciar-api.sh
```

En las siguientes ocasiones basta ejecutar `./iniciar-api.sh` desde la raíz.
Detén la API con `Ctrl+C`.

La API estará disponible en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.

En Windows PowerShell, activa el entorno virtual con:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Iniciar el frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Abre `http://localhost:5173` en el navegador.

## Configuración

El frontend usa la variable `VITE_API_URL` para conocer la URL base de la API. El valor local por defecto es:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Puedes cambiarla en `frontend/.env` para usar otro host o un ambiente remoto.

La configuración del backend se define con variables que comienzan con `APP_`; consulta `backend/.env.example` para ver los valores disponibles.


## API

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Estado general del servicio. |
| `GET` | `/api/v1/heartbeat` | Comprobación liviana de disponibilidad. |
| `GET` | `/api/v1/products` | Lista los productos disponibles. |
| `POST` | `/api/v1/cart/calculate` | Calcula subtotales y total usando los precios vigentes del catálogo. |

Ejemplo para calcular una bolsa:

```json
{
  "items": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 2, "quantity": 1 }
  ]
}
```

## Comandos de desarrollo

### Frontend

```bash
cd frontend
npm run dev      # servidor de desarrollo
npm run build    # verificación de tipos y build de producción
npm run lint     # análisis estático
```

### Backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload  # servidor de desarrollo
pytest                          # pruebas automatizadas
ruff check .                    # análisis estático
ruff format --check .           # validación de formato
```

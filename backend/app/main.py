from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.health_controller import router as health_router
from app.controllers.product_controller import router as product_router
from app.core.config import settings
from app.models.product import ProductRepository


def create_app(database_path: str | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""
    repository = ProductRepository(database_path or settings.database_path)
    repository.initialize()

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="API REST para el taller DevOps.",
    )
    application.state.product_repository = repository

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health_router, prefix=settings.api_prefix)
    application.include_router(product_router, prefix=settings.api_prefix)

    return application


app = create_app()

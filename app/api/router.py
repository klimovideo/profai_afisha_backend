from fastapi import APIRouter

from .routers import cities, creations

router = APIRouter()
router.include_router(cities.router, tags=['Города'])
router.include_router(creations.router, tags=['Произведения'])

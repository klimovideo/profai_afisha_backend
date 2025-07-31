from fastapi import APIRouter
from .routers import cities, creations, places, promotions

router = APIRouter()
router.include_router(cities.router, tags=["Города"])
router.include_router(creations.router, tags=["Произведения"])
router.include_router(places.router, tags=["Площадки"])
router.include_router(promotions.router, tags=["Промоакции"])

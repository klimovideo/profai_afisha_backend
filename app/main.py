from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router
from app.core.config import settings
from app.services.afisha import AfishaClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.afisha_client = AfishaClient()  # Initialize AfishaClient
    yield
    await app.state.afisha_client.close()  # Close AfishaClient on shutdown


app = FastAPI(
    title=settings.app_name,
    description='Сервис для работы с API Афиши',
    version=settings.version,
    lifespan=lifespan,
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

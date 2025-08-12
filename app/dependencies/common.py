# app/dependencies/afisha.py

from fastapi import Request
from app.services.afisha import AfishaClient


async def get_afisha_client(request: Request) -> AfishaClient:
    return request.app.state.afisha_client

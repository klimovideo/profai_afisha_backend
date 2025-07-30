from fastapi import Request
from app.services.afisha_client import AfishaClient

def get_afisha_client(request: Request) -> AfishaClient:
    afisha = request.app.state.afisha_client
    if not afisha:
        raise ValueError("AfishaClient is not initialized in the application state.")
    return afisha

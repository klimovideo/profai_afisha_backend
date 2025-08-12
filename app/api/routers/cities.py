from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.common import get_afisha_client
from app.schemas.cities import CitiesRequest
from app.schemas.cities import CitiesFilter
from app.services.afisha import AfishaClient
from app.utils.logger import get_logger
from app.utils.helpers import transform_params

router = APIRouter()
logger = get_logger(__name__)


@router.get('/cities')
async def get_cities(
    params: CitiesFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        request_params = transform_params(params=params.model_dump())
        response = await afisha.cities.get_list(request_params)
        return response
    except Exception:
        logger.error('Ошибка при получении списка городов', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/city/{city_id}')
async def get_city(
    city_id: int,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        response = await afisha.cities.get_by_id(city_id)
        return response
    except Exception:
        logger.error(f'Ошибка при получении города с ID {city_id}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')

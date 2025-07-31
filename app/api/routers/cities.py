from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.afisha import get_afisha_client
from app.schemas.cities import CitiesFilter
from app.services.afisha import AfishaClient
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get('/cities')
async def get_cities(
    filters: CitiesFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        cities = await afisha.cities.get_list(**filters.model_dump(exclude_none=True))
        logger.info(f'Успешно получено городов: {len(cities)}')
        return cities
    except Exception as e:
        logger.error(f'Ошибка при получении списка городов: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/city/{city_id}')
async def get_city(city_id: int, afisha: AfishaClient = Depends(get_afisha_client)):
    try:
        city = await afisha.cities.get_by_id(city_id)
        logger.info(f'Успешно получен город: {city.get("Name", "Unknown")}')
        return city
    except Exception as e:
        logger.error(f'Ошибка при получении города с city_id={city_id}: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')

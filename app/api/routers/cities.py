from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.afisha import get_afisha_client
from app.services.afisha import AfishaClient
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get('/cities')
async def get_cities(
    date_from=None,
    date_to=None,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    """Запрос возвращает все города с открытыми продажами для вашего партнерского аккаунта. По умолчанию возвращаются для всех продаж, начиная с текущей даты, при указании периода - только за указанный период"""
    try:
        logger.info('Запрос: получение списка городов')
        cities = await afisha.cities.get_list(date_from, date_to)
        logger.info(f'Успешно получено городов: {len(cities)}')
        return cities
    except Exception as e:
        logger.error(f'Ошибка при получении списка городов: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/city/{city_id}')
async def get_city(city_id: int, afisha: AfishaClient = Depends(get_afisha_client)):
    """Получение города по идентификатору. Не зависит от наличия открытых продаж"""
    try:
        logger.info(f'Запрос: получение города по Id={city_id}')
        city = await afisha.cities.get_by_id(city_id)
        logger.info(f'Успешно получен город: {city["Name"]}')
        return city
    except Exception as e:
        logger.error(f'Ошибка при получении города по Id: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

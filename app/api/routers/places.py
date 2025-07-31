import logging

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from app.dependencies.afisha import get_afisha_client
from app.services.afisha import AfishaClient
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get('/places')
async def get_places(
    city_id: int,
    date_from=None,
    date_to=None,
    creation_type=None,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    """По умолчанию возвращаются площадки для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
    try:
        logger.info(f'Запрос: получение списка площадок для города c Id={city_id}')
        places = await afisha.places.get_list(city_id, date_from, date_to, creation_type)
        logger.info(f'Успешно получено площадок: {len(places)}')
        return places
    except Exception as e:
        logger.error(f'Ошибка при получении площадок: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/place/{id}')
async def get_place(id, afisha: AfishaClient = Depends(get_afisha_client)):
    """Получение площадки по идентификатору, не учитывает доступность продаж"""
    try:
        logger.info(f'Запрос: получение площадки c Id={id}')
        place = await afisha.places.get_by_id(id)
        logger.info(f'Успешно получена площадка: {place["Name"]}')
        return place
    except Exception as e:
        logger.error(f'Ошибка при получении площадки: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/place/{id}/schedule')
async def get_place_schedule(
    id,
    date_from=None,
    date_to=None,
    cinema_format_date_from=None,
    cinema_format_date_to=None,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    """Получение расписания площадки по идентификатору с необязательной фильтрацией по дате сеанса"""
    try:
        logger.info(f'Запрос: получение расписания площадки c Id={id}')
        schedule = await afisha.places.get_schedule_by_id(
            id,
            date_from=None,
            date_to=None,
            cinema_format_date_from=None,
            cinema_format_date_to=None,
        )
        logger.info(f'Успешно получено расписание площадки. Элементов: {len(schedule)}')
        return schedule
    except Exception as e:
        logger.error(f'Ошибка при получении расписания площадки: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

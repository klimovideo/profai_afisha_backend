from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.afisha import get_afisha_client
from app.services.afisha import AfishaClient
from app.schemas.places import PlacesFilter, PlaceScheduleFilter
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get('/places')
async def get_places(
    filter: PlacesFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        places = await afisha.places.get_list(**filter.model_dump(exclude_none=True))
        logger.info(f'Успешно получено площадок: {len(places)}')
        return places
    except Exception as e:
        logger.error(f'Ошибка при получении площадок: {str(e)}')
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/place/{id}')
async def get_place(id, afisha: AfishaClient = Depends(get_afisha_client)):
    try:
        place = await afisha.places.get_by_id(id)
        logger.info(f'Успешно получена площадка: {place["Name"]}')
        return place
    except Exception as e:
        logger.error(f'Ошибка при получении площадки: {str(e)}')
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/place/{id}/schedule')
async def get_place_schedule(
    id,
    filter: PlaceScheduleFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        schedule = await afisha.places.get_schedule_by_id(
            id,
            **filter.model_dump(exclude_none=True),
        )
        logger.info(f'Успешно получено расписание площадки. Элементов: {len(schedule)}')
        return schedule
    except Exception as e:
        logger.error(f'Ошибка при получении расписания площадки: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

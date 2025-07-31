from fastapi import APIRouter, Body, Depends, HTTPException, Query

from app.dependencies.afisha import get_afisha_client
from app.schemas.creations import CreationsFilter, CreationsScheduleFilter
from app.services.afisha import AfishaClient
from app.utils.preprocess import clean_creations
from app.utils.helpers import get_city_id
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get('/creations/page')  ### ОСНОВНОЙ ЭНДПОИНТ ДЛЯ БОТА
async def get_creations(
    filter: CreationsFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        city_id = get_city_id(filter.city_name, from_api=True)
        if city_id is None:
            raise HTTPException(status_code=404, detail='Город не найден')

        creations = await afisha.creations.get_list(**filter.model_dump(exclude_none=True))
        logger.info(f'Успешно получено произведений: {len(creations["Creations"])}')
        return clean_creations(creations)
    except Exception as e:
        logger.error(f'Ошибка при получении списка произведений: {str(e)}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


# @router.post('/creations/page')
# async def get_creations_post(
#     request: CreationsRequest = Body(...), afisha: AfishaClient = Depends(get_afisha_client)
# ):
#     try:
#         city_id = request.city_id
#         city_name = request.city_name
#         date_from = request.date_from
#         date_to = request.date_to
#         creation_type = request.creation_type
#         limit = request.limit
#         cursor = request.cursor

#         if city_id is None and city_name is not None:
#             city_id = get_city_id(city_name, from_api=True)
#             if city_id is None:
#                 raise HTTPException(status_code=404, detail='Город не найден')
#         elif city_id is None and city_name is None:
#             raise HTTPException(status_code=400, detail='Необходимо указать city_id или city_name')

#         logger.info(f'Запрос: получение произведения для города {city_id}, страница {cursor}')
#         creations = await afisha.creations.get_list(
#             city_id, date_from, date_to, creation_type, limit, cursor
#         )
#         logger.info(f'Успешно получено произведений: {len(creations["Creations"])}')
#         return preprocess_creations(creations)
#     except Exception as e:
#         logger.error(f'Ошибка при получении произведений: {str(e)}')
#         raise HTTPException(status_code=500, detail=str(e))


@router.get('/creation/{id}')
async def get_creation(
    id,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        creation = await afisha.creations.get_by_id(id)
        logger.info(f'Успешно получено произведение: {creation["Name"]}')
        return creation
    except Exception as e:
        logger.info(f'Ошибка при получении произведения: {str(e)}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/creation/kinoplan/{id}')
async def get_creation_kinoplan(
    id,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        creation = await afisha.creations.get_by_kinoplan_id(id)
        logger.info(f'Успешно получено произведение: {creation["Name"]}')
        return creation
    except Exception as e:
        logger.info(f'Ошибка при получении произведения Kinoplan: {str(e)}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/creation/{id}/schedule')
async def get_creation_schedule(
    id,
    filter: CreationsScheduleFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    """Получение расписания произведения по идентификатору с необязательной фильтрацией по дате сеанса"""
    try:
        logger.info(f'Запрос: получение расписания произведения по Id={id}')
        schedule = afisha.creations.get_schedule(id, **filter.model_dump(exclude_none=True))
        logger.info(f'Успешно получено расписание произведения. Элементов: {len(schedule)}')
        return schedule
    except Exception as e:
        logger.info(f'Ошибка при получении расписания произведения Kinoplan: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from app.dependencies.afisha import get_afisha_client
from app.models.schemas import CreationsRequest
from app.services.afisha import AfishaClient
from app.utils.clean_json import preprocess_creations
from app.utils.get_city import get_city_id
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get('/creations/page')  ### ОСНОВНОЙ ЭНДПОИНТ ДЛЯ БОТА
async def get_creations(
    city_id: int = Query(None, description='ID города для поиска произведений.'),
    city_name: str = Query(None, description='Название города (альтернатива city_id).'),
    date_from: str = Query(None, description='Дата начала периода в формате date-time.'),
    date_to: str = Query(None, description='Дата окончания периода в формате date-time.'),
    creation_type: str = Query(
        None,
        description="Тип произведения ('Concert', 'Performance', 'UserEvent', 'Excursion', 'Movie', 'Event', 'Admission', 'SportEvent'",
    ),
    limit: int = Query(None, description='Количество элементов на странице.'),
    cursor: str = Query(None, description='Курсор для пагинации.'),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    """По умолчанию возвращаются произведения для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
    try:
        if city_id is None and city_name is not None:
            # Получаем id по названию города
            city_id = get_city_id(city_name, from_api=True)
            if city_id is None:
                raise HTTPException(status_code=404, detail='Город не найден')
        elif city_id is None and city_name is None:
            raise HTTPException(status_code=400, detail='Необходимо указать city_id или city_name')

        logger.info(f'Запрос: получение произведения для города {city_id}, страница {cursor}')
        creations = await afisha.creations.get_list(
            city_id, date_from, date_to, creation_type, limit, cursor
        )
        logger.info(f'Успешно получено произведений: {len(creations["Creations"])}')
        # return creations
        return preprocess_creations(creations)
    except Exception as e:
        logger.error(f'Ошибка при получении произведений: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/creations/page')
async def get_creations_post(
    request: CreationsRequest = Body(...), afisha: AfishaClient = Depends(get_afisha_client)
):
    try:
        city_id = request.city_id
        city_name = request.city_name
        date_from = request.date_from
        date_to = request.date_to
        creation_type = request.creation_type
        limit = request.limit
        cursor = request.cursor

        if city_id is None and city_name is not None:
            city_id = get_city_id(city_name, from_api=True)
            if city_id is None:
                raise HTTPException(status_code=404, detail='Город не найден')
        elif city_id is None and city_name is None:
            raise HTTPException(status_code=400, detail='Необходимо указать city_id или city_name')

        logger.info(f'Запрос: получение произведения для города {city_id}, страница {cursor}')
        creations = await afisha.creations.get_list(
            city_id, date_from, date_to, creation_type, limit, cursor
        )
        logger.info(f'Успешно получено произведений: {len(creations["Creations"])}')
        return preprocess_creations(creations)
    except Exception as e:
        logger.error(f'Ошибка при получении произведений: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/creation/{id}')
async def get_creation(
    id,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    """Получение произведения по Id, не учитывает доступность продаж"""
    try:
        logger.info(f'Запрос: получение произведения по Id={id}')
        creation = await afisha.creations.get_by_id(id)
        logger.info(f'Успешно получено произведение: {creation["Name"]}')
        return creation
    except Exception as e:
        logger.info(f'Ошибка при получении произведения: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/creation/kinoplan/{id}')
async def get_creation_kinoplan(
    id,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    """Получение произведения по идентификатору Kinoplan, не учитывает доступность продаж"""
    try:
        logger.info(f'Запрос: получение произведения по Kinoplan Id={id}')
        creation = await afisha.creations.get_by_kinoplan_id(id)
        logger.info(f'Успешно получено произведение: {creation["Name"]}')
        return creation
    except Exception as e:
        logger.info(f'Ошибка при получении произведения Kinoplan: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/creation/{id}/schedule')
async def get_creation_schedule(
    id,
    city_id=None,
    date_from=None,
    date_to=None,
    cinema_format_date_from=None,
    cinema_format_date_to=None,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    """Получение расписания произведения по идентификатору с необязательной фильтрацией по дате сеанса"""
    try:
        logger.info(f'Запрос: получение расписания произведения по Id={id}')
        schedule = afisha.creations.get_schedule(
            id, city_id, date_from, date_to, cinema_format_date_from, cinema_format_date_to
        )
        logger.info(f'Успешно получено расписание произведения. Элементов: {len(schedule)}')
        return schedule
    except Exception as e:
        logger.info(f'Ошибка при получении расписания произведения Kinoplan: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

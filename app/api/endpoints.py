import logging

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from app.dependencies.afisha import get_afisha_client
from app.models.schemas import CreationsRequest
from app.services.afisha_client import AfishaClient
from app.utils.clean_json import preprocess_creations
from app.utils.get_city import get_city_id

logger = logging.getLogger(__name__)

router = APIRouter()


# Эндпоинты
# -------------------- Эндпоинты для городов --------------------


@router.get('/cities')
async def get_cities(
    date_from=None,
    date_to=None,
    afisha_client: AfishaClient = Depends(get_afisha_client),
):
    """Запрос возвращает все города с открытыми продажами для вашего партнерского аккаунта. По умолчанию возвращаются для всех продаж, начиная с текущей даты, при указании периода - только за указанный период"""
    try:
        logger.info('Запрос: получение списка городов')
        cities = await afisha_client.get_cities(date_from, date_to)
        logger.info(f'Успешно получено городов: {len(cities)}')
        return cities
    except Exception as e:
        logger.error(f'Ошибка при получении списка городов: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/city/{city_id}')
async def get_city(city_id: int, afisha_client: AfishaClient = Depends(get_afisha_client)):
    """Получение города по идентификатору. Не зависит от наличия открытых продаж"""
    try:
        logger.info(f'Запрос: получение города по Id={city_id}')
        city = await afisha_client.get_city(city_id)
        logger.info(f'Успешно получен город: {city["Name"]}')
        return city
    except Exception as e:
        logger.error(f'Ошибка при получении города по Id: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


# -------------------- Эндпоинты для произведений (событий, мероприятий, фильмов и т.д.) --------------------


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
    afisha_client: AfishaClient = Depends(get_afisha_client),
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
        creations = await afisha_client.get_creations(
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
    request: CreationsRequest = Body(...), afisha_client: AfishaClient = Depends(get_afisha_client)
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
        creations = await afisha_client.get_creations(
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
    afisha_client: AfishaClient = Depends(get_afisha_client),
):
    """Получение произведения по Id, не учитывает доступность продаж"""
    try:
        logger.info(f'Запрос: получение произведения по Id={id}')
        creation = await afisha_client.get_creation(id)
        logger.info(f'Успешно получено произведение: {creation["Name"]}')
        return creation
    except Exception as e:
        logger.info(f'Ошибка при получении произведения: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/creation/kinoplan/{id}')
async def get_creation_kinoplan(
    id,
    afisha_client: AfishaClient = Depends(get_afisha_client),
):
    """Получение произведения по идентификатору Kinoplan, не учитывает доступность продаж"""
    try:
        logger.info(f'Запрос: получение произведения по Kinoplan Id={id}')
        creation = await afisha_client.get_creation_kinoplan(id)
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
    afisha_client: AfishaClient = Depends(get_afisha_client),
):
    """Получение расписания произведения по идентификатору с необязательной фильтрацией по дате сеанса"""
    try:
        logger.info(f'Запрос: получение расписания произведения по Id={id}')
        schedule = afisha_client.get_creation_schedule(
            id, city_id, date_from, date_to, cinema_format_date_from, cinema_format_date_to
        )
        logger.info(f'Успешно получено расписание произведения. Элементов: {len(schedule)}')
        return schedule
    except Exception as e:
        logger.info(f'Ошибка при получении расписания произведения Kinoplan: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


# -------------------- Эндпоинты для площадок (мест событий) --------------------


@router.get('/places')
async def get_places(
    city_id: int,
    date_from=None,
    date_to=None,
    creation_type=None,
    afisha_client: AfishaClient = Depends(get_afisha_client),
):
    """По умолчанию возвращаются площадки для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
    try:
        logger.info(f'Запрос: получение списка площадок для города c Id={city_id}')
        places = await afisha_client.get_places(city_id, date_from, date_to, creation_type)
        logger.info(f'Успешно получено площадок: {len(places)}')
        return places
    except Exception as e:
        logger.error(f'Ошибка при получении площадок: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/place/{id}')
async def get_place(id, afisha_client: AfishaClient = Depends(get_afisha_client)):
    """Получение площадки по идентификатору, не учитывает доступность продаж"""
    try:
        logger.info(f'Запрос: получение площадки c Id={id}')
        place = await afisha_client.get_place(id)
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
    afisha_client: AfishaClient = Depends(get_afisha_client),
):
    """Получение расписания площадки по идентификатору с необязательной фильтрацией по дате сеанса"""
    try:
        logger.info(f'Запрос: получение расписания площадки c Id={id}')
        schedule = await afisha_client.get_place_schedule(
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


# -------------------- Эндпоинты для промоакций --------------------


@router.get('/promotions')
async def get_promotions(
    availability=None, afisha_client: AfishaClient = Depends(get_afisha_client)
):
    """Получение списка действующих промоакций"""
    try:
        logger.info('Запрос: получение действующих промоакций')
        promotions = await afisha_client.get_promotions(availability)
        logger.info(f'Успешно получены промоакции: {len(promotions)}')
        return promotions
    except Exception as e:
        logger.error(f'Ошибка при получении промоакций: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/promotion/{id}/sessions')
async def get_promotion_sessions(
    id, city_id, afisha_client: AfishaClient = Depends(get_afisha_client)
):
    """Получение списка сеансов, на которые действует указанная промоакция. Возвращается не более 150000 сеансов"""
    try:
        logger.info('Запрос: получение списка сеансов промоакции')
        sessions = await afisha_client.get_promotion_sessions(id, city_id)
        logger.info(f'Успешно получены сеансы промоакции: {len(sessions)}')
        return sessions
    except Exception as e:
        logger.error(f'Ошибка при получении сеансов промоакции: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

import sys
import os
import logging

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from afisha_client import AfishaClient

sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
from get_city import get_city_id
from clean_json import preprocess_creations


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('afisha_api.log')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Afisha API Service",
    description="Сервис для работы с API Афиши",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация клиента Афиши
afisha_client = AfishaClient()

# Эндпоинты
#-------------------- Эндпоинты для городов --------------------

@app.get("/cities")
async def get_cities(date_from=None, date_to=None):
    """Запрос возвращает все города с открытыми продажами для вашего партнерского аккаунта. По умолчанию возвращаются для всех продаж, начиная с текущей даты, при указании периода - только за указанный период"""
    try:
        logger.info("Запрос: получение списка городов")
        cities = afisha_client.get_cities(date_from, date_to)
        logger.info(f"Успешно получено городов: {len(cities)}")
        return cities
    except Exception as e:
        logger.error(f"Ошибка при получении списка городов: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/city/{city_id}")
async def get_city(city_id: int):
    """Получение города по идентификатору. Не зависит от наличия открытых продаж"""
    try:
        logger.info(f"Запрос: получение города по Id={city_id}")
        city = afisha_client.get_city(city_id)
        logger.info(f"Успешно получен город: {city['Name']}")
        return city
    except Exception as e:
        logger.error(f"Ошибка при получении города по Id: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
#-------------------- Эндпоинты для произведений (событий, мероприятий, фильмов и т.д.) --------------------

@app.get("/creations/page")
async def get_creations(
            city_id: int = Query(None, description="ID города для поиска произведений."),
            city_name: str = Query(None, description="Название города (альтернатива city_id)."),
            date_from: str = Query(None, description="Дата начала периода в формате date-time."),
            date_to: str = Query(None, description="Дата окончания периода в формате date-time."),
            creation_type: str = Query(None, description="Тип произведения ('Concert', 'Performance', 'UserEvent', 'Excursion', 'Movie', 'Event', 'Admission', 'SportEvent'"),
            limit: int = Query(None, description="Количество элементов на странице."),
            cursor: str = Query(None, description="Курсор для пагинации.")
):
    """По умолчанию возвращаются произведения для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
    try:
        if city_id is None and city_name is not None:
            # Получаем id по названию города
            city_id = get_city_id(city_name, from_api=True)
            if city_id is None:
                raise HTTPException(status_code=404, detail="Город не найден")
        elif city_id is None and city_name is None:
            raise HTTPException(status_code=400, detail="Необходимо указать city_id или city_name")
        
        logger.info(f"Запрос: получение произведения для города {city_id}, страница {cursor}")
        creations = afisha_client.get_creations(city_id, date_from, date_to, creation_type, limit, cursor)
        logger.info(f"Успешно получено произведений: {len(creations['Creations'])}")
        # return creations
        return preprocess_creations(creations)
    except Exception as e:
        logger.error(f"Ошибка при получении произведений: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/creation/{id}")
async def get_creation(id):
    """Получение произведения по Id, не учитывает доступность продаж"""
    try:
        logger.info(f"Запрос: получение произведения по Id={id}")
        creation = afisha_client.get_creation(id)
        logger.info(f"Успешно получено произведение: {creation['Name']}")
        return creation
    except Exception as e:
        logger.info(f"Ошибка при получении произведения: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/creation/kinoplan/{id}")
async def get_creation_kinoplan(id):
    """Получение произведения по идентификатору Kinoplan, не учитывает доступность продаж"""
    try:
        logger.info(f"Запрос: получение произведения по Kinoplan Id={id}")
        creation = afisha_client.get_creation_kinoplan(id)
        logger.info(f"Успешно получено произведение: {creation['Name']}")
        return creation
    except Exception as e:
        logger.info(f"Ошибка при получении произведения Kinoplan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/creation/{id}/schedule")
async def get_creation_schedule(id, city_id=None, date_from=None, date_to=None, cinema_format_date_from=None, cinema_format_date_to=None):
    """Получение расписания произведения по идентификатору с необязательной фильтрацией по дате сеанса"""
    try:
        logger.info(f"Запрос: получение расписания произведения по Id={id}")
        schedule = afisha_client.get_creation_schedule(id, city_id, date_from, date_to, cinema_format_date_from, cinema_format_date_to)
        logger.info(f"Успешно получено расписание произведения. Элементов: {len(schedule)}")
        return schedule
    except Exception as e:
        logger.info(f"Ошибка при получении расписания произведения Kinoplan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
#-------------------- Эндпоинты для площадок (мест событий) --------------------
    
@app.get("/places")
async def get_places(city_id: int, date_from=None, date_to=None, creation_type=None):
    """По умолчанию возвращаются площадки для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
    try:
        logger.info(f"Запрос: получение списка площадок для города c Id={city_id}")
        places = afisha_client.get_places(city_id, date_from, date_to, creation_type)
        logger.info(f"Успешно получено площадок: {len(places)}")
        return places
    except Exception as e:
        logger.error(f"Ошибка при получении площадок: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/place/{id}")
async def get_place(id):
    """Получение площадки по идентификатору, не учитывает доступность продаж"""
    try:
        logger.info(f"Запрос: получение площадки c Id={id}")
        place = afisha_client.get_place(id)
        logger.info(f"Успешно получена площадка: {place['Name']}")
        return place
    except Exception as e:
        logger.error(f"Ошибка при получении площадки: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/place/{id}/schedule")
async def get_place_schedule(id, date_from=None, date_to=None, cinema_format_date_from=None, cinema_format_date_to=None):
    """Получение расписания площадки по идентификатору с необязательной фильтрацией по дате сеанса"""
    try:
        logger.info(f"Запрос: получение расписания площадки c Id={id}")
        schedule = afisha_client.get_place_schedule(id, date_from=None, date_to=None, cinema_format_date_from=None, cinema_format_date_to=None)
        logger.info(f"Успешно получено расписание площадки. Элементов: {len(schedule)}")
        return schedule
    except Exception as e:
        logger.error(f"Ошибка при получении расписания площадки: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

#-------------------- Эндпоинты для промоакций --------------------

@app.get("/promotions")
async def get_promotions(availability=None):
    """Получение списка действующих промоакций"""
    try:
        logger.info(f"Запрос: получение действующих промоакций")
        promotions = afisha_client.get_promotions(availability)
        logger.info(f"Успешно получены промоакции: {len(promotions)}")
        return promotions
    except Exception as e:
        logger.error(f"Ошибка при получении промоакций: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/promotion/{id}/sessions")
async def get_promotion_sessions(id, city_id):
    """Получение списка сеансов, на которые действует указанная промоакция. Возвращается не более 150000 сеансов"""
    try:
        logger.info(f"Запрос: получение списка сеансов промоакции")
        sessions = afisha_client.get_promotion_sessions(id, city_id)
        logger.info(f"Успешно получены сеансы промоакции: {len(sessions)}")
        return sessions
    except Exception as e:
        logger.error(f"Ошибка при получении сеансов промоакции: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

#-------------------- Ручка для мероприятий по городу --------------------
# @app.get("/events")
# async def get_events_city(name_city):
#     """Получение мероприятий по названию города"""
#     try:
#         logger.info(f"Запрос: получение списка мероприятий по названию города")
#
#     except Exception as e:
#         logger.error(f"Ошибка при получении сеансов промоакции: {str(e)}")
#         raise HTTPException(status_code=500, )

if __name__ == "__main__":
    import uvicorn
    logger.info("Запуск сервера Afisha API")
    uvicorn.run(app, host="0.0.0.0", port=8001) 
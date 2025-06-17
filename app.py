from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from afisha_client import AfishaClient
import logging
import sys

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
@app.get("/cities")
async def get_cities():
    """Получить список доступных городов"""
    try:
        logger.info("Запрос: получение списка городов")
        cities = afisha_client.get_cities()
        logger.info(f"Успешно получено {len(cities)} городов")
        return cities
    except Exception as e:
        logger.error(f"Ошибка при получении списка городов: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/city/{city_id}")
async def get_city(city_id: int):
    """Получить город по его Id"""
    try:
        logger.info(f"Запрос: получение города по Id {city_id}")
        city = afisha_client.get_city(city_id)
        logger.info(f"Успешно получен город {city['Name']}")
        return city
    except Exception as e:
        logger.error(f"Ошибка при получении города по Id: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/{city_id}")
async def get_events(city_id: int, page: int = 1, per_page: int = 20):
    """Получить список событий для конкретного города"""
    try:
        logger.info(f"Запрос: получение событий для города {city_id}, страница {page}")
        events = afisha_client.get_events(city_id, page, per_page)
        logger.info(f"Успешно получено {len(events.get('items', []))} событий")
        return events
    except Exception as e:
        logger.error(f"Ошибка при получении событий: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/{city_id}/{event_id}")
async def get_event_details(city_id: int, event_id: int):
    """Получить детальную информацию о событии"""
    try:
        logger.info(f"Запрос: получение информации о событии {event_id} в городе {city_id}")
        event = afisha_client.get_event_details(event_id)
        logger.info(f"Успешно получена информация о событии {event_id}")
        return event
    except Exception as e:
        logger.error(f"Ошибка при получении информации о событии: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Запуск сервера Afisha API")
    uvicorn.run(app, host="0.0.0.0", port=8001) 
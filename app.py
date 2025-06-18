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

@app.get("/creations/page")
async def get_creations(city_id: int, date_from=None, date_to=None, creation_type=None, limit=None, cursor=None):
    """Получить список произведений для конкретного города с разбивкой по страницам"""
    try:
        logger.info(f"Запрос: получение произведения для города {city_id}, страница {cursor}")
        creations = afisha_client.get_creations(city_id, date_from, date_to, creation_type, limit, cursor)
        logger.info(f"Успешно получено {len(creations['Creations'])} произведений")
        # logger.info("Успешно получено")
        return creations
    except Exception as e:
        logger.error(f"Ошибка при получении событий: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    logger.info("Запуск сервера Afisha API")
    uvicorn.run(app, host="0.0.0.0", port=8001) 
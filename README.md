# Afisha API Service

Веб-сервис для работы с API Афиши, построенный на FastAPI.

## Структура папок

```
afisha_api/
├── app/
│   ├── api/ # Маршруты и роутеры FastAPI
│   │   ├── router.py
│   │   └── routers/
│   ├── core/ # Конфигурация приложения
│   ├── dependencies/ # Зависимости FastAPI
│   ├── main.py # Точка входа приложения
│   ├── schemas/# Pydantic-схемы
│   ├── services/ # Логика работы с афишой
│   │   └── afisha/
│   ├── tests/ # Тесты и тестовые данные
│   │   └── data/
│   └── utils/ # Вспомогательные функции и логгер
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Документация API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

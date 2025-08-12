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

## Установка на сервере

1. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` в корневой директории проекта:
```
PARTNER_KEY=ваш_ключ_партнера
WIDGET_KEY=ваш_ключ_виджета
```

## Настройка systemd сервиса

1. Скопируйте файл конфигурации systemd:
```bash
sudo cp afisha-api.service /etc/systemd/system/
```

2. Перезагрузите конфигурацию systemd:
```bash
sudo systemctl daemon-reload
```

3. Включите автозапуск сервиса:
```bash
sudo systemctl enable afisha-api
```

4. Запустите сервис:
```bash
sudo systemctl start afisha-api
```

5. Проверьте статус сервиса:
```bash
sudo systemctl status afisha-api
```

## Управление сервисом

- Запуск: `sudo systemctl start afisha-api`
- Остановка: `sudo systemctl stop afisha-api`
- Перезапуск: `sudo systemctl restart afisha-api`
- Просмотр логов: `sudo journalctl -u afisha-api -f`

## API Endpoints

### Документация API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

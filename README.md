# Afisha API Service

Веб-сервис для работы с API Афиши, построенный на FastAPI.

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

### Доступные эндпоинты:

1. `GET /cities`
   - Получить список доступных городов

2. `GET /events/{city_id}`
   - Получить список событий для конкретного города
   - Параметры:
     - `page` (опционально): номер страницы (по умолчанию 1)
     - `per_page` (опционально): количество событий на странице (по умолчанию 20)

3. `GET /events/{city_id}/{event_id}`
   - Получить детальную информацию о конкретном событии

## Примеры использования

### Получение списка городов
```bash
curl http://localhost:8000/cities
```

### Получение событий в городе
```bash
curl http://localhost:8000/events/1?page=1&per_page=20
```

### Получение информации о событии
```bash
curl http://localhost:8000/events/1/123
``` 
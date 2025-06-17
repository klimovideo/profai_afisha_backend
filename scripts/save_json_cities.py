import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from afisha_client import AfishaClient

def save_cities_to_json():
    # Создаем клиент Афиши
    client = AfishaClient()
    
    try:
        # Получаем список городов
        cities = client.get_cities()
        
        # Создаем имя файла с текущей датой и временем
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # filename = f"data/cities_{timestamp}.json"
        filename = f"data/cities.json"
         
        # Сохраняем в JSON файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cities, f, ensure_ascii=False, indent=2)
        
        print(f"Список городов успешно сохранен в файл: {filename}")
        print(f"Всего сохранено городов: {len(cities)}")
        
    except Exception as e:
        print(f"Произошла ошибка при сохранении городов: {str(e)}")

if __name__ == "__main__":
    save_cities_to_json()

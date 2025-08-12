from datetime import date, datetime, time, timedelta
from typing import Optional, Any


def _get_city_id(city_name: str, cities: dict):
    cities = cities.get('Cities', []) if isinstance(cities, dict) else cities

    for city in cities:
        if city['Name'] == city_name:
            return city['Id']
    return None


def _convert_dates(
    date_from: Optional[date] | Optional[str], date_to: Optional[date] | Optional[str]
) -> tuple[Optional[datetime], Optional[datetime]]:
    def to_datetime(d):
        if isinstance(d, str):
            d = datetime.strptime(d, '%Y-%m-%d').date()
        return datetime.combine(d, time.min) if d else None

    date_from_dt = to_datetime(date_from)
    date_to_dt = to_datetime(date_to)

    if date_from_dt and date_to_dt and date_from_dt == date_to_dt:
        date_to_dt += timedelta(days=1)

    return date_from_dt, date_to_dt


def _to_camel_case(snake: str) -> str:
    parts = snake.split('_')
    return ''.join(p.capitalize() for p in parts)


def transform_params(params: dict[str, Any], cities: Optional[dict] = None) -> dict[str, Any]:
    """Преобразует входные параметры запроса в формат, необходимый для API Афишы.

    Args:
        params (dict[str, Any]): Параметры запроса:
        cities (Optional[dict], optional): Если передан данный параметр, то нужно найти id города из этого списка.

    Returns:
        dict[str, Any]: _Преобразованные параметры запроса для API Афишы.
    """
    out_params = {}

    # Обработка города
    city_name = params.get('city_name')
    city_id = params.get('city_id')

    if cities and city_name:
        out_params['CityId'] = _get_city_id(city_name, cities)
    elif city_id:
        out_params['CityId'] = city_id

    date_from_raw = params.get('date_from')
    date_to_raw = params.get('date_to')

    if date_from_raw or date_to_raw:
        date_from, date_to = _convert_dates(date_from_raw, date_to_raw)

        if date_from:
            out_params['DateFrom'] = date_from.isoformat()
        if date_to:
            out_params['DateTo'] = date_to.isoformat()

    # keys_afisha = ['CityId', 'DateFrom', 'DateTo', 'CreationType', 'Limit', 'Cursor', 'CinemaFormatDateFrom', 'CinemaFormatDateTo']
    passthrough_keys = ['creation_type', 'limit', 'cursor']  # Прочие поля
    for key in passthrough_keys:
        if key in params:
            out_params[_to_camel_case(key)] = params[key]

    return out_params


def clean_creations(creations):
    elements = creations['Creations']

    all_keys = [
        'AfishaPriority',
        'Genres',
        'Duration',
        'Rating',
        'KinoplanId',
        'Images',
        'ProductionYear',
        'Name',
        'AfishaCreationUrl',
        'Videos',
        'ReleaseDate',
        'ShortDescription',
        'Description',
        'AfishaId',
        'AgeRestriction',
        'AfishaClassId',
        'MainPhotoCrops',
        'Id',
        'Participants',
        'Country',
        'Type',
        'DurationDescription',
    ]

    need_keys = [
        'Id',
        'Type',
        'Name',
        'Genres',
        'Description',
        'Rating',
        'ReleaseDate',
        'AgeRestriction',
        'Country',
        'AfishaId',
        'AfishaCreationUrl',
    ]

    filtered = []
    for element in elements:
        filtered_element = {k: element[k] for k in need_keys if k in element}
        filtered.append(filtered_element)
    return filtered

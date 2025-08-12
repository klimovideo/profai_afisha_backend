from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.common import get_afisha_client
from app.schemas.creations import CreationFilter, CreationScheduleFilter
from app.services.afisha import AfishaClient
from app.utils.helpers import clean_creations, transform_params
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get('/creations/page')
async def get_creations(
    params: CreationFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        cities_response = await afisha.cities.get_list()
        request_params = transform_params(params=params, cities=cities_response)
        response = clean_creations(await afisha.creations.get_list(request_params))
        return response
    except Exception:
        logger.error('Ошибка при получении списка произведений', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/creation/{id}')
async def get_creation(
    id,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        response = await afisha.creations.get_by_id(id)
        return response
    except Exception:
        logger.error(f'Ошибка при получении произведения с ID {id}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/creation/kinoplan/{id}')
async def get_creation_kinoplan(
    id,
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        response = await afisha.creations.get_by_kinoplan_id(id)
        return response
    except Exception:
        logger.error(f'Ошибка при получении произведения с Kinoplan ID {id}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@router.get('/creation/{id}/schedule')
async def get_creation_schedule(
    id,
    params: CreationScheduleFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        cities_response = await afisha.cities.get_list()
        request_params = transform_params(params=params, cities=cities_response)
        response = await afisha.creations.get_schedule(id, params=request_params)
        return response
    except Exception:
        logger.error(f'Ошибка при получении расписания произведения с ID {id}', exc_info=True)
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')

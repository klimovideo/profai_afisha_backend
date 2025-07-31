import logging

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from app.dependencies.afisha import get_afisha_client
from app.services.afisha import AfishaClient

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/promotions')
async def get_promotions(
    availability=None, afisha: AfishaClient = Depends(get_afisha_client)
):
    """Получение списка действующих промоакций"""
    try:
        logger.info('Запрос: получение действующих промоакций')
        promotions = await afisha.promotions.get_list(availability)
        logger.info(f'Успешно получены промоакции: {len(promotions)}')
        return promotions
    except Exception as e:
        logger.error(f'Ошибка при получении промоакций: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/promotion/{id}/sessions')
async def get_promotion_sessions(
    id, city_id, afisha: AfishaClient = Depends(get_afisha_client)
):
    """Получение списка сеансов, на которые действует указанная промоакция. Возвращается не более 150000 сеансов"""
    try:
        logger.info('Запрос: получение списка сеансов промоакции')
        sessions = await afisha.promotions.get_sessions(id, city_id)
        logger.info(f'Успешно получены сеансы промоакции: {len(sessions)}')
        return sessions
    except Exception as e:
        logger.error(f'Ошибка при получении сеансов промоакции: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

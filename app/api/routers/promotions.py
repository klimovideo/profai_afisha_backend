from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.afisha import get_afisha_client
from app.services.afisha import AfishaClient
from app.schemas.promotions import PromotionsFilter, PromotionSessionFilter
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get('/promotions')
async def get_promotions(
    filter: PromotionsFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        promotions = await afisha.promotions.get_list(**filter.model_dump(exclude_none=True))
        logger.info(f'Успешно получены промоакции: {len(promotions)}')
        return promotions
    except Exception as e:
        logger.error(f'Ошибка при получении промоакций: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/promotion/{id}/sessions')
async def get_promotion_sessions(
    id,
    filter: PromotionSessionFilter = Depends(),
    afisha: AfishaClient = Depends(get_afisha_client),
):
    try:
        sessions = await afisha.promotions.get_sessions(id, **filter.model_dump(exclude_none=True))
        logger.info(f'Успешно получены сеансы промоакции: {len(sessions)}')
        return sessions
    except Exception as e:
        logger.error(f'Ошибка при получении сеансов промоакции: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

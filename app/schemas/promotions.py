from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class PromotionsFilter(BaseModel):
    availability: Optional[bool] = Field(
        default=None,
        description='Фильтр по доступности промоакций. Если True, возвращаются только доступные промоакции.',
        example=True,
    )


class PromotionSessionFilter(BaseModel):
    city_id: str = Field(
        ...,
        description='Идентификатор города, для которого нужно получить сеансы.',
        example='city456',
    )

    @field_validator('city_id')
    def validate_ids(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            raise ValueError(f'{info.field_name} не может быть пустым')
        return value

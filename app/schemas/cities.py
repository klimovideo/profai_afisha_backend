from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class CitiesFilter(BaseModel):
    date_from: Optional[date] = Field(
        default=None,
        description='Дата начала периода (формат YYYY-MM-DD)',
        example='2024-08-01',
    )
    date_to: Optional[date] = Field(
        default=None,
        description='Дата окончания периода (формат YYYY-MM-DD)',
        example='2024-08-15',
    )

    @field_validator('date_to')
    def check_date_range(cls, date_to_value, info: ValidationInfo):
        date_from_value = info.data.get('date_from')
        if date_to_value and date_from_value and date_to_value < date_from_value:
            raise ValueError('date_to не может быть раньше date_from')
        return date_to_value


# class CityFilter(BaseModel):
#     city_id: int = Field(description='Идентификатор города', example=1)

#     @field_validator('city_id')
#     def check_city_id(cls, city_id_value):
#         if city_id_value <= 0:
#             raise ValueError('city_id должен быть положительным целым числом')
#         return city_id_value

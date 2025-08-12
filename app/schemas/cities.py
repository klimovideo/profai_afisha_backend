from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class CitiesFilter(BaseModel): # Фильтрация параметров получаемые самой FastAPI
    date_from: Optional[date] = Field(None, description='Дата начала периода (формат YYYY-MM-DD)')
    date_to: Optional[date] = Field(None, description='Дата окончания периода (формат YYYY-MM-DD)')

    # @field_validator('date_to')
    # def check_date_range(cls, date_to_value, info: ValidationInfo):
    #     date_from_value = info.data.get('date_from')
    #     if date_to_value and date_from_value and date_to_value < date_from_value:
    #         raise ValueError('date_to не может быть раньше date_from')
    #     return date_to_value


class CitiesRequest(BaseModel): # Фильтрация параметров отправляемые в сервис Афиши
    DateFrom: Optional[datetime] = None
    DateTo: Optional[datetime] = None

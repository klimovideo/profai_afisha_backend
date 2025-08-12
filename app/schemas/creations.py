from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class CreationFilter(BaseModel):  # Фильтрация параметров получаемые самой FastAPI
    city_id: Optional[int] = Field(None, description='ID города для поиска')
    city_name: Optional[str] = Field(None, description='Название города.')
    date_from: Optional[str] = Field(
        None, description='Дата начала периода в формате (YYYY-MM-DD).'
    )
    date_to: Optional[str] = Field(
        None, description='Дата окончания периода в формате (YYYY-MM-DD).'
    )
    creation_type: Optional[str] = Field(
        None, description="Тип произведения 'Concert', 'Movie' и т.д."
    )
    limit: Optional[int] = Field(None, description='Количество элементов на странице.', ge=1)
    cursor: Optional[str] = Field(None, description='Курсор для пагинации.')

    @field_validator('date_to')
    def validate_date_range(cls, v, info: ValidationInfo):
        date_from = info.data.get('date_from')
        if v and date_from and v < date_from:
            raise ValueError('date_to не может быть раньше date_from')
        return v


class CreationScheduleFilter(BaseModel):  # Фильтрация параметров получаемые самой FastAPI
    city_id: Optional[int] = Field(
        None, description='ID города, по которому фильтруется расписание.'
    )
    city_name: Optional[str] = Field(None, description='Название города.')
    date_from: Optional[str] = Field(None, description='Дата начала расписания (формат YYYY-MM-DD)')
    date_to: Optional[str] = Field(
        None, description='Дата окончания расписания (формат YYYY-MM-DD)'
    )
    cinema_format_date_from: Optional[str] = Field(
        None, description='Начальная дата для форматированных дат кинотеатра (формат YYYY-MM-DD)'
    )
    cinema_format_date_to: Optional[str] = Field(
        None, description='Конечная дата для форматированных дат кинотеатра (формат YYYY-MM-DD)'
    )

    @field_validator('date_to')
    def validate_date_range(cls, v, info: ValidationInfo):
        date_from = info.data.get('date_from')
        if v and date_from and v < date_from:
            raise ValueError('date_to не может быть раньше date_from')
        return v

    @field_validator('cinema_format_date_to')
    def validate_cinema_format_date_range(cls, v, info: ValidationInfo):
        d_from = info.data.get('cinema_format_date_from')
        if v and d_from and v < d_from:
            raise ValueError('cinema_format_date_to не может быть раньше cinema_format_date_from')
        return v


class CreationsRequest(BaseModel):  # Фильтрация параметров отправляемые в сервис Афиши
    CityId: Optional[int] = None
    DateFrom: Optional[datetime] = None
    DateTo: Optional[datetime] = None
    CreationType: Optional[str] = None
    Limit: Optional[int] = None
    Cursor: Optional[str] = None


class CreationScheduleRequest(BaseModel):  # Фильтрация параметров отправляемые в сервис Афиши
    CityId: Optional[int] = None
    DateFrom: Optional[datetime] = None
    DateTo: Optional[datetime] = None
    CinemaFormatDateFrom: Optional[datetime] = None
    CinemaFormatDateTo: Optional[datetime] = None

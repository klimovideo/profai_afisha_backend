from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class CreationFilter(BaseModel):
    city_id: Optional[int] = Field(
        None,
        description='ID города для поиска произведений.',
        example=123,
    )
    city_name: Optional[str] = Field(
        None,
        description='Название города.',
        example='Москва',
    )
    date_from: Optional[str] = Field(
        None,
        description='Дата начала периода в формате (YYYY-MM-DD).',
        example='2024-08-01',
    )
    date_to: Optional[str] = Field(
        None,
        description='Дата окончания периода в формате (YYYY-MM-DD).',
        example='2024-08-15',
    )
    creation_type: Optional[str] = Field(
        None,
        description="Тип произведения (например, 'Concert', 'Performance', 'Movie', 'Event' и т.д.).",
        example='Movie',
    )
    limit: Optional[int] = Field(
        None,
        description='Количество элементов на странице.',
        example=10,
        ge=1,
    )
    cursor: Optional[str] = Field(
        None,
        description='Курсор для пагинации.',
        example='abc123',
    )

    @field_validator('date_to')
    def validate_date_range(cls, v, info: ValidationInfo):
        date_from = info.data.get('date_from')
        if v and date_from and v < date_from:
            raise ValueError('date_to не может быть раньше date_from')
        return v


class CreationScheduleFilter(BaseModel):
    city_id: Optional[int] = Field(
        default=None,
        description='ID города, по которому фильтруется расписание.',
        example=6,
    )
    city_name: Optional[str] = Field(
        default=None,
        description='Название города, по которому фильтруется расписание.',
        example='Москва',
    )
    date_from: Optional[str] = Field(
        default=None,
        description='Дата начала периода расписания (формат YYYY-MM-DD)',
        example='2024-08-01',
    )
    date_to: Optional[str] = Field(
        default=None,
        description='Дата окончания периода расписания (формат YYYY-MM-DD)',
        example='2024-08-15',
    )
    cinema_format_date_from: Optional[str] = Field(
        default=None,
        description='Начальная дата для форматированных дат кинотеатра (формат YYYY-MM-DD)',
        example='2024-08-01',
    )
    cinema_format_date_to: Optional[str] = Field(
        default=None,
        description='Конечная дата для форматированных дат кинотеатра (формат YYYY-MM-DD)',
        example='2024-08-10',
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

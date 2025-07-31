from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class PlacesFilter(BaseModel):
    city_id: int = Field(
        None,
        description='ID города для поиска площадок.',
        example=123,
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

    @field_validator('date_to')
    def validate_date_range(cls, v, info: ValidationInfo):
        date_from = info.data.get('date_from')
        if v and date_from and v < date_from:
            raise ValueError('date_to не может быть раньше date_from')
        return v


class PlaceScheduleFilter(BaseModel):
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
    cinema_format_date_from: Optional[str] = Field(
        None,
        description='Дата начала периода в формате (YYYY.MM.DD).',
        example='2024.08.01',
    )
    cinema_format_date_to: Optional[str] = Field(
        None,
        description='Дата окончания периода в формате (YYYY.MM.DD).',
        example='2024.08.15',
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

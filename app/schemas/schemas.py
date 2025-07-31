# app/models/base.py
from pydantic import BaseModel
from typing import Optional, List


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


# app/models/city.py
class CityResponse(BaseSchema):
    id: int
    name: str


# app/models/creation.py
class CreationsFilter(BaseSchema):
    city_id: Optional[int] = None
    city_name: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    creation_type: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


class CreationsRequest(BaseSchema):
    city_id: Optional[int]
    city_name: Optional[str]
    date_from: Optional[str]
    date_to: Optional[str]
    creation_type: Optional[str]
    limit: Optional[int]
    cursor: Optional[str]


# app/models/place.py
class PlacesFilter(BaseSchema):
    city_id: int
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    creation_type: Optional[str] = None


# app/models/promotion.py
class PromotionSessionsFilter(BaseSchema):
    city_id: int

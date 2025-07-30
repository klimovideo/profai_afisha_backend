from pydantic import BaseModel
from typing import Optional

class CreationsRequest(BaseModel):
    city_id: Optional[int] = None
    city_name: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    creation_type: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None
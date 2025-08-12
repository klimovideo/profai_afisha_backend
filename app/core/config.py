from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Параметры FastAPI
    app_name: str = 'Backend Afisha API Service'
    version: str = '1.0.0'
    host: str = '0.0.0.0'
    port: int = 8000

    # Логирование
    log_level: str = 'INFO'
    log_file: str = 'afisha_api.log'

    # Внешний API Афиши
    afisha_api_key: str = Field(..., env='AFISHA_API_KEY')
    afisha_widget_key: str = Field(..., env='AFISHA_WIDGET_KEY')
    afisha_base_url: str = 'https://api.afisha.ru/v1'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

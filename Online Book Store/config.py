from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    DATABASE_URL : str
    SECRET_KEY : str
    APP_PORT: int

    class Config:
        env_file = ".env"

settings = Setting()        
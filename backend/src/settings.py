from pydantic import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    # environment: str
    database_url: str = "sqlite:///db.sqlite"
    connect_args: dict = {"check_same_thread": False}
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
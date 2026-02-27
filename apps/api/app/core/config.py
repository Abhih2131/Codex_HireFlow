from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WorkplaceAI HireFlow API"
    database_url: str = "postgresql+psycopg2://hireflow:hireflow@localhost:5432/hireflow"
    secret_key: str = "dev-secret"
    access_token_expire_minutes: int = 60 * 24
    otp_ttl_minutes: int = 10
    dev_otp: str = "123456"
    uploads_dir: str = "apps/api/uploads"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

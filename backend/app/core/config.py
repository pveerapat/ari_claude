from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ARI Backend"
    APP_ENV: str = "local"
    APP_DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "ari_local"
    POSTGRES_USER: str = "ari_user"
    POSTGRES_PASSWORD: str = "change_me_local_only"
    DATABASE_URL: str = "postgresql+psycopg://ari_user:change_me_local_only@postgres:5432/ari_local"

    JWT_SECRET_KEY: str = "change_me_local_only"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ROOT_USER: str = "ari_minio_user"
    MINIO_ROOT_PASSWORD: str = "change_me_local_only"
    MINIO_BUCKET: str = "ari-local"
    MINIO_SECURE: bool = False

    EMQX_HOST: str = "emqx"
    EMQX_MQTT_PORT: int = 1883
    EMQX_DASHBOARD_PORT: int = 18083
    EMQX_USERNAME: str = "ari_emqx_user"
    EMQX_PASSWORD: str = "change_me_local_only"

    CORS_ALLOW_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    CORS_ALLOW_CREDENTIALS: bool = True

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "plain"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

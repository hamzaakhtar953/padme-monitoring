from typing import Literal

from keycloak import KeycloakOpenID
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        extra="ignore",
    )

    ENVIRONMENT: Literal["local", "production"] = "local"

    PROJECT_NAME: str
    DOMAIN: str

    DB_URL_DATABASE: str
    DB_URL_HOST: str
    DB_URL_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str

    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str


settings = Settings()

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    realm_name=settings.KEYCLOAK_REALM,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)

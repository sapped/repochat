# created per instructions: https://testdriven.io/blog/fastapi-docker-traefik/

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    deeplake_username: str = Field(..., env="DEEPLAKE_USERNAME")
    deeplake_dataset_name: str = Field(..., env="DEEPLAKE_DATASET_NAME")
    activeloop_token: str = Field(..., env="ACTIVELOOP_TOKEN")


settings = Settings()

# 1. про Settings знает все наше приложение(domain, logic, infra, api)
# 2. здесь хранятся все наши константы, конектион стринг и и т.д.
from pydantic import Field
from pydantic_settings import BaseSettings
import os


class Config(BaseSettings):
    # mongodb_connection_uri: str = Field(os.getenv("MONGODB_CONNECTION_URI"))  # забираем с .env
    mongodb_connection_uri: str = "mongodb://mongodb:27017"
    # mongodb_connection_uri: str = Field(alias="MONGODB_CONNECTION_URI")  # забираем с .env

    mongo_db_db_name: str = Field(default='chat_db', alias="MONGODB_CHAT_DATABASE")
    mongo_db_collection_name: str = Field(default='chat_collection', alias='MONGODB_CHAT_COLLECTION')

    class Config:
        env_file = "../../.env"
        env_file_encoding = 'utf-8'

    print(f"mongodb_connection_uri={mongodb_connection_uri}")
    print(f"mongo_db_db_name={mongo_db_db_name}")
    print(f"mongo_db_collection_name={mongo_db_collection_name}")





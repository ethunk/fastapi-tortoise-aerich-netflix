import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

SQLITE_DB_URL = "sqlite://:memory:"
TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

def init_db(app: FastAPI, is_test: bool = False) -> None:

    if is_test:
        db_url = os.environ['DATABASE_URL'] + '_test'
    else:
        db_url = os.environ['DATABASE_URL']

    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

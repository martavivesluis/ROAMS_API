from fastapi import FastAPI
from api.routes.client import client_router
from api.routes.mortgage import mortgage_router
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()
app.include_router(client_router)
app.include_router(mortgage_router)

register_tortoise(
    app = app,
    db_url = "sqlite://db",
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"models":["api.models.client","api.models.mortgage"]}
)



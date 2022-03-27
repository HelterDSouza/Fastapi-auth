from fastapi import FastAPI

from app.core import settings


def get_application() -> FastAPI:
    application = FastAPI(**settings.fastapi_kwargs)


    return application


app = get_application()

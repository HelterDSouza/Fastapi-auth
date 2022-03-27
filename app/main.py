from fastapi import FastAPI

from app.core import settings
from app.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    application = FastAPI(**settings.fastapi_kwargs)

    application.add_event_handler(
        "startup", create_start_app_handler(application, settings)
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )
    return application


app = get_application()

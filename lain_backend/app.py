from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from lain_backend import __version__, config
from lain_backend.events import startup, shutdown

from lain_backend.blueprints import api


def create_app() -> FastAPI:
    app = FastAPI(title="Lain Backend", version=__version__, debug=config.DEBUG)

    register_middlewares(app)
    register_routes(app)
    register_events(app)

    return app


def register_routes(app: FastAPI):
    app.include_router(api.router, prefix="/api")


def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=("http://localhost:3000",),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_events(app: FastAPI):
    app.on_event("startup")(startup)
    app.on_event("shutdown")(shutdown)

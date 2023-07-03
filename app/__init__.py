import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials
from starlette.middleware.cors import CORSMiddleware

from app.config import ROUTER_CONFIGS, settings
from app.constants import DEFAULT_ROUTER_SETTINGS
from app.model import CommonResponseModel
from app.mongo import init_mongo


def create_app() -> FastAPI:
    google_keep_app: FastAPI = FastAPI(
        version=settings.API_VERSION,
        description=settings.API_DESCRIPTION,
        title=settings.API_TITLE,
    )
    google_keep_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return google_keep_app


app: FastAPI = create_app()


@app.on_event("startup")
async def startup_event():
    cred = credentials.Certificate("creds/firebase.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "keep-424a4.appspot.com"})
    await init_mongo(settings)


@app.get(
    "/",
    tags=["Health"],
    **DEFAULT_ROUTER_SETTINGS,
)
async def root() -> CommonResponseModel:
    return CommonResponseModel(
        status="success",
        message="Welcome to Google Keep API",
    )


@app.get(
    "/health",
    tags=["Health"],
    **DEFAULT_ROUTER_SETTINGS,
)
async def health() -> CommonResponseModel:
    return CommonResponseModel(
        status="success",
        message="Health check passed",
    )


for config in ROUTER_CONFIGS.configs:
    app.include_router(
        config.router,
        prefix=config.prefix,
    )

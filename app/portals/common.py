from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from ..db import engine

APP_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


def new_portal(name: str) -> FastAPI:
    portal = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    portal.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")

    @portal.get("/healthz")
    def healthz():
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "portal": name}

    return portal

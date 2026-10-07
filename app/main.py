from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from .config import settings
from .db import engine

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

# Hostname decides which portal is served. Unknown hosts get 404.
PORTALS = {
    settings.shop_host: "shop",
    settings.app_host: "app",
    settings.admin_host: "admin",
}

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.middleware("http")
async def resolve_portal(request: Request, call_next):
    host = request.headers.get("host", "").split(":")[0].lower()
    portal = PORTALS.get(host)
    if portal is None:
        return PlainTextResponse("Not found", status_code=404)
    request.state.portal = portal
    return await call_next(request)


@app.get("/healthz")
def healthz(request: Request):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "portal": request.state.portal}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    portal = request.state.portal
    return templates.TemplateResponse(request, f"{portal}/home.html", {"portal": portal})

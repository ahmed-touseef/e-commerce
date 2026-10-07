from fastapi import Request
from fastapi.responses import HTMLResponse

from .common import new_portal, templates

vendor = new_portal("app")


@vendor.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "app/home.html", {})

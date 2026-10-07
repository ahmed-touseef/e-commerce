from fastapi import Request
from fastapi.responses import HTMLResponse

from .common import new_portal, templates

shop = new_portal("shop")


@shop.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "shop/home.html", {})

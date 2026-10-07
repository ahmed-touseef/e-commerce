from starlette.applications import Starlette
from starlette.routing import Host

from .config import settings
from .portals.admin import admin
from .portals.shop import shop
from .portals.vendor import vendor

# The hostname decides which portal answers. Any other host gets 404.
app = Starlette(routes=[
    Host(settings.shop_host, app=shop),
    Host(settings.app_host, app=vendor),
    Host(settings.admin_host, app=admin),
])

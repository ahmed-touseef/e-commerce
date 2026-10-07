from datetime import datetime, timezone

from fastapi import Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func, select
from starlette.middleware.sessions import SessionMiddleware

from ..config import settings
from ..db import SessionLocal
from ..models import AdminUser
from ..security import LoginThrottle, csrf_ok, csrf_token, hash_password, needs_rehash, verify_password
from .common import new_portal, templates

admin = new_portal("admin")
admin.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="ef_admin",
    max_age=12 * 60 * 60,
    same_site="lax",
    https_only=True,
)

throttle = LoginThrottle()


def current_admin(request: Request, db) -> AdminUser | None:
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return None
    user = db.get(AdminUser, admin_id)
    if user is None or not user.is_active:
        request.session.clear()
        return None
    return user


def render(request: Request, name: str, ctx: dict, status: int = 200):
    ctx = {"csrf": csrf_token(request), **ctx}
    return templates.TemplateResponse(request, name, ctx, status_code=status)


@admin.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    with SessionLocal() as db:
        if current_admin(request, db):
            return RedirectResponse("/", status_code=303)
    return render(request, "admin/login.html", {"email": "", "error": None})


@admin.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(""), password: str = Form(""), csrf: str = Form("")):
    ip = request.client.host if request.client else "unknown"
    email = email.strip().lower()

    if not csrf_ok(request, csrf):
        return render(request, "admin/login.html",
                      {"email": email, "error": "Sessione scaduta. Riprova."}, 400)
    if throttle.blocked(ip):
        return render(request, "admin/login.html",
                      {"email": email, "error": "Troppi tentativi. Riprova tra 15 minuti."}, 429)

    with SessionLocal() as db:
        user = db.scalar(select(AdminUser).where(func.lower(AdminUser.email) == email))
        ok = verify_password(user.password_hash if user else None, password)
        if not ok or not user.is_active:
            throttle.fail(ip)
            return render(request, "admin/login.html",
                          {"email": email, "error": "Email o password non corretti."}, 400)

        if needs_rehash(user.password_hash):
            user.password_hash = hash_password(password)
        user.last_login_at = datetime.now(timezone.utc)
        db.commit()
        user_id = user.id

    throttle.reset(ip)
    request.session.clear()
    request.session["admin_id"] = user_id
    return RedirectResponse("/", status_code=303)


@admin.post("/logout")
def logout(request: Request, csrf: str = Form("")):
    if csrf_ok(request, csrf):
        request.session.clear()
    return RedirectResponse("/login", status_code=303)


@admin.get("/", response_class=HTMLResponse)
def home(request: Request):
    with SessionLocal() as db:
        user = current_admin(request, db)
        if user is None:
            return RedirectResponse("/login", status_code=303)
        return render(request, "admin/home.html", {"user": user, "nav": "home"})

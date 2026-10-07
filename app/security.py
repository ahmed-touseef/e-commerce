import secrets
import time
from collections import defaultdict, deque

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import Request

_hasher = PasswordHasher()
_DUMMY_HASH = _hasher.hash("timing-equaliser-not-a-real-password")


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str | None, password: str) -> bool:
    """Constant effort check. Pass None for an unknown user."""
    try:
        return _hasher.verify(password_hash or _DUMMY_HASH, password) and password_hash is not None
    except (VerificationError, InvalidHashError):
        return False


def needs_rehash(password_hash: str) -> bool:
    return _hasher.check_needs_rehash(password_hash)


def csrf_token(request: Request) -> str:
    token = request.session.get("csrf")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf"] = token
    return token


def csrf_ok(request: Request, submitted: str | None) -> bool:
    expected = request.session.get("csrf")
    return bool(expected and submitted and secrets.compare_digest(expected, submitted))


class LoginThrottle:
    """At most `limit` failed logins per IP within `window` seconds (per process)."""

    def __init__(self, limit: int = 10, window: int = 900):
        self.limit = limit
        self.window = window
        self._fails: dict[str, deque] = defaultdict(deque)

    def _trim(self, ip: str) -> deque:
        q = self._fails[ip]
        cutoff = time.monotonic() - self.window
        while q and q[0] < cutoff:
            q.popleft()
        return q

    def blocked(self, ip: str) -> bool:
        return len(self._trim(ip)) >= self.limit

    def fail(self, ip: str) -> None:
        self._trim(ip).append(time.monotonic())

    def reset(self, ip: str) -> None:
        self._fails.pop(ip, None)

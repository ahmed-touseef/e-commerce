"""Admin account management.

Usage, from ~/eurofiora-shop:
    .venv/bin/python -m app.cli create-admin
Creates an admin, or resets the password if the email already exists.
"""
import getpass
import sys

from sqlalchemy import func, select

from .db import SessionLocal
from .models import AdminUser
from .security import hash_password

MIN_LEN = 10


def create_admin() -> int:
    email = input("Email: ").strip().lower()
    if "@" not in email:
        print("Not a valid email.")
        return 1
    with SessionLocal() as db:
        user = db.scalar(select(AdminUser).where(func.lower(AdminUser.email) == email))
        name = input(f"Name [{user.name if user else ''}]: ").strip() or (user.name if user else "")
        if not name:
            print("Name is required.")
            return 1
        pw = getpass.getpass(f"Password (min {MIN_LEN} characters): ")
        if len(pw) < MIN_LEN:
            print("Password too short.")
            return 1
        if getpass.getpass("Repeat password: ") != pw:
            print("Passwords do not match.")
            return 1
        if user:
            user.name = name
            user.password_hash = hash_password(pw)
            user.is_active = True
            action = "updated"
        else:
            db.add(AdminUser(email=email, name=name, password_hash=hash_password(pw)))
            action = "created"
        db.commit()
    print(f"Admin {email} {action}.")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["create-admin"]:
        sys.exit(create_admin())
    print(__doc__)
    sys.exit(1)

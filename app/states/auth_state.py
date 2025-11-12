import reflex as rx
import bcrypt
import logging
import datetime
from typing import TypedDict
from sqlmodel import text


class User(TypedDict):
    id: int
    username: str
    email: str
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserInfo(TypedDict):
    id: int
    username: str
    email: str
    created_at: str
    updated_at: str


class AuthState(rx.State):
    token: str | None = rx.Cookie(name="token")
    error_message: str = ""
    show_user_menu: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.token is not None

    @rx.var
    def user_id(self) -> int | None:
        if not self.is_authenticated or not self.token:
            return None
        try:
            parts = self.token.split("_")
            if len(parts) > 1 and parts[-1].isdigit():
                return int(parts[-1])
            return None
        except (ValueError, IndexError) as e:
            logging.exception(f"Error parsing user_id from token: {e}")
            return None

    @rx.var
    def user_info(self) -> UserInfo:
        default_user = UserInfo(
            id=0, username="Guest", email="", created_at="", updated_at=""
        )
        if not self.is_authenticated or self.user_id is None:
            return default_user
        with rx.session() as session:
            result = session.exec(
                text(
                    'SELECT id, username, email, created_at, updated_at FROM "user" WHERE id = :user_id'
                ),
                {"user_id": self.user_id},
            ).first()
            if result:
                return UserInfo(
                    id=result.id,
                    username=result.username,
                    email=result.email,
                    created_at=result.created_at.isoformat(),
                    updated_at=result.updated_at.isoformat(),
                )
        return default_user

    @rx.event
    def toggle_user_menu(self):
        self.show_user_menu = not self.show_user_menu

    @rx.event
    async def register(self, form_data: dict):
        username = form_data.get("username", "").strip()
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        confirm_password = form_data.get("confirm_password", "").strip()
        self.error_message = ""
        if password != confirm_password:
            self.error_message = "Passwords do not match."
            return
        if not all([username, email, password]):
            self.error_message = "All fields are required."
            return
        try:
            with rx.session() as session:
                existing_user = session.exec(
                    text(
                        'SELECT id FROM "user" WHERE username = :username OR email = :email'
                    ),
                    {"username": username, "email": email},
                ).first()
                if existing_user:
                    self.error_message = "Username or email already exists."
                    return
                hashed_password = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                session.exec(
                    text(
                        'INSERT INTO "user" (username, email, hashed_password, created_at, updated_at) VALUES (:username, :email, :hashed_password, :created_at, :updated_at)'
                    ),
                    {
                        "username": username,
                        "email": email,
                        "hashed_password": hashed_password,
                        "created_at": datetime.datetime.now(datetime.timezone.utc),
                        "updated_at": datetime.datetime.now(datetime.timezone.utc),
                    },
                )
                session.commit()
            return rx.redirect("/login")
        except Exception as e:
            logging.exception(f"Registration failed: {e}")
            self.error_message = "An unexpected error occurred during registration."

    @rx.event
    async def login(self, form_data: dict):
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        self.error_message = ""
        if not email or not password:
            self.error_message = "Email and password are required."
            return
        try:
            with rx.session() as session:
                user_result = session.exec(
                    text('SELECT id, hashed_password FROM "user" WHERE email = :email'),
                    {"email": email},
                ).first()
                if user_result and bcrypt.checkpw(
                    password.encode("utf-8"),
                    user_result.hashed_password.encode("utf-8"),
                ):
                    self.token = f"token_for_user_{user_result.id}"
                    return rx.redirect("/")
                else:
                    self.error_message = "Invalid email or password."
                    return
        except Exception as e:
            logging.exception(f"Login failed: {e}")
            self.error_message = "An unexpected error occurred during login."

    @rx.event
    def logout(self):
        self.token = None
        self.show_user_menu = False
        return rx.redirect("/login")


@rx.event
async def require_login(state: rx.State) -> rx.event.EventSpec | None:
    auth_state = await state.get_state(AuthState)
    if not auth_state.is_authenticated:
        return rx.redirect("/login")
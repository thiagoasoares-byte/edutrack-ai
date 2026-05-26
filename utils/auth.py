"""
Auth helpers for Streamlit session management.
"""
import streamlit as st
import utils.api as api


def is_logged_in() -> bool:
    return bool(st.session_state.get("auth_token"))


def require_auth():
    """Call at the top of any protected page. Redirects to login if not authenticated."""
    if not is_logged_in():
        st.warning("🔒 Você precisa estar logado para acessar esta página.")
        st.stop()


def login(email: str, password: str):
    """Attempt login; on success stores token and user in session."""
    data = api.post("auth", "/login", {"email": email, "password": password})
    st.session_state["auth_token"] = data["auth_token"]
    st.session_state["user"] = data["user"]
    return data["user"]


def signup(name: str, email: str, password: str):
    """Register a new user and log them in."""
    data = api.post("auth", "/signup", {"name": name, "email": email, "password": password})
    st.session_state["auth_token"] = data["auth_token"]
    st.session_state["user"] = data["user"]
    return data["user"]


def logout():
    for key in ["auth_token", "user"]:
        st.session_state.pop(key, None)


def current_user() -> dict:
    return st.session_state.get("user", {})

"""
Centralized Xano API helper.
All requests go through here, automatically attaching the auth token from session.
"""
import streamlit as st
import requests
from typing import Optional

# Default Xano instance for this project — requests will always point here by default.
# This makes the frontend work without needing a .env file. If you ever need to
# override in a special environment, you can change this constant.
INSTANCE = "x8ki-letl-twmt"
BASE_URL = f"https://{INSTANCE}.n7.xano.io/api"

# Request timeout (seconds)
DEFAULT_TIMEOUT = 15

GROUPS = {
    "auth":           f"{BASE_URL}:auth",
    "subjects":       f"{BASE_URL}:subjects",
    "academic_tasks": f"{BASE_URL}:academic_tasks",
}


def _headers():
    token = st.session_state.get("auth_token", "")
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _handle(resp: requests.Response):
    """Raise on HTTP error, return parsed JSON or None."""
    if resp.status_code == 204:
        return {"success": True}
    try:
        data = resp.json()
    except Exception:
        data = {}
    if not resp.ok:
        msg = data.get("message") or data.get("error") or f"HTTP {resp.status_code}"
        raise RuntimeError(msg)
    return data


def get(group: str, path: str, params: Optional[dict] = None):
    url = f"{GROUPS[group]}{path}"
    resp = requests.get(url, headers=_headers(), params=params or {}, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def post(group: str, path: str, body: Optional[dict] = None):
    url = f"{GROUPS[group]}{path}"
    resp = requests.post(url, headers=_headers(), json=body or {}, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def patch(group: str, path: str, body: Optional[dict] = None):
    url = f"{GROUPS[group]}{path}"
    resp = requests.patch(url, headers=_headers(), json=body or {}, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def delete(group: str, path: str, params: Optional[dict] = None):
    url = f"{GROUPS[group]}{path}"
    resp = requests.delete(url, headers=_headers(), params=params or {}, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)

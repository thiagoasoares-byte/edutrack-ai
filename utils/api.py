"""
Centralized Xano API helper.
All requests go through here, automatically attaching the auth token from session.
"""
import os
import streamlit as st
import requests
from typing import Optional

# Allow runtime override of the Xano workspace URL.
# If the default workspace is no longer active, set API_BASE_URL in the environment:
#   API_BASE_URL="https://<your-instance>.n7.xano.io/api"
# Or set XANO_INSTANCE for the legacy workspace identifier.
API_BASE_URL = os.environ.get("API_BASE_URL")
INSTANCE = os.environ.get("XANO_INSTANCE", "x8ki-letl-twmt")
BASE_URL = API_BASE_URL.rstrip("/") if API_BASE_URL else f"https://{INSTANCE}.n7.xano.io/api"

# Request timeout (seconds)
DEFAULT_TIMEOUT = 15

# Enable verbose API logging when set to true in the environment.
DEBUG_API = os.environ.get("EDUTRACK_DEBUG_API", "0") in ("1", "true", "True")

GROUP_CANONICAL_IDS = {
    "auth": "yMJziCve",
    "subject": "yCLJBTsI", # Changed from 'subjects' to 'subject' as per canonical name in guide
    "academic_tasks": "academic_tasks",
}

# Construct the full group base URLs using the canonical IDs
GROUPS = {
    group: f"{BASE_URL}:{canonical_id}"
    for group, canonical_id in GROUP_CANONICAL_IDS.items()
}


def _headers():
    token = st.session_state.get("auth_token", "")
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _handle(resp: requests.Response):
    """Raise on HTTP error, return parsed JSON or None."""
    if DEBUG_API:
        try:
            print(f"[api] RESPONSE {resp.status_code} {resp.url} -> {resp.text}")
        except Exception:
            pass
    if resp.status_code == 204:
        return {"success": True}
    try:
        data = resp.json()
    except Exception:
        data = {}
    if not resp.ok:
        msg = None
        if isinstance(data, dict):
            msg = data.get("message") or data.get("error") or data.get("errors")
        if not msg:
            msg = resp.text.strip() or f"HTTP {resp.status_code}"
        raise RuntimeError(msg)
    return data


def _normalize_path(path: str) -> str:
    """Normalize a user-provided path to always use forward slashes and start with '/'."""
    if not path:
        return ""
    p = path.replace("\\", "/")
    if not p.startswith("/"):
        p = "/" + p
    return p


def get(group: str, path:str, params: Optional[dict] = None):
    path = _normalize_path(path)
    url = f"{GROUPS[group]}{path}"
    if DEBUG_API:
        print(f"[api] GET {url} params={params}")
    resp = requests.get(url, headers=_headers(), params=params or {}, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def post(group: str, path: str, body: Optional[dict] = None):
    path = _normalize_path(path)
    url = f"{GROUPS[group]}{path}"
    if DEBUG_API:
        print(f"[api] POST {url} body={body}")
    resp = requests.post(url, headers=_headers(), json=body or {}, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def patch(group: str, path: str, body: Optional[dict] = None):
    path = _normalize_path(path)
    url = f"{GROUPS[group]}{path}"
    if DEBUG_API:
        print(f"[api] PATCH {url} body={body}")
    resp = requests.patch(url, headers=_headers(), json=body or {}, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def delete(group: str, path: str, params: Optional[dict] = None):
    path = _normalize_path(path)
    url = f"{GROUPS[group]}{path}"
    if DEBUG_API:
        print(f"[api] DELETE {url} params={params}")
    resp = requests.delete(url, headers=_headers(), params=params or {}, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)

import streamlit as st


def _css():
    return """
    <style>
    :root{
      --bg:#0f1724; /* deep navy */
      --card:#0b1220;
      --muted:#9aa7b2;
      --accent:#6ee7b7; /* teal */
      --accent-2:#7dd3fc;
      --glass: rgba(255,255,255,0.03);
    }
    .stApp {
      background: linear-gradient(180deg, #071021 0%, #0b1220 100%);
      color: #e6eef6;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    .page-header { padding: 14px 18px; border-radius: 10px; background: linear-gradient(90deg, rgba(125,211,252,0.06), rgba(110,231,183,0.04)); margin-bottom:12px }
    .page-title { color: var(--accent); font-weight:700; margin:0; font-size:28px }
    .page-sub { color: var(--muted); margin:0; font-size:13px }
    .card { background: var(--card); padding:12px; border-radius:10px; box-shadow: 0 6px 18px rgba(2,6,23,0.6); }
    .muted { color: var(--muted) }
    .accent-btn { background: linear-gradient(90deg,var(--accent),var(--accent-2)); color:#052022; border:none; padding:8px 12px; border-radius:8px }
    .sidebar .stButton>button { border-radius:8px }
    </style>
    """


def apply_theme(page_title: str = None, page_icon: str = None, layout: str = "wide"):
    if page_title or page_icon or layout:
        try:
            st.set_page_config(page_title=page_title or "EduTrack", page_icon=page_icon or "📚", layout=layout)
        except Exception:
            pass
    st.markdown(_css(), unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"<div class='page-header'><h1 class='page-title'>{title}</h1><div class='page-sub'>{subtitle}</div></div>", unsafe_allow_html=True)


def sidebar_logout_button():
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True):
            return True
    return False

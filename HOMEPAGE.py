import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import utils.api as api
import utils.auth as auth
from datetime import date, datetime

st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎓 EduTrack AI")
    if auth.is_logged_in():
        user = auth.current_user()
        st.markdown(f"**👤 {user.get('name', 'Usuário')}**")
        st.markdown(f"_{user.get('email', '')}_")
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True):
            auth.logout()
            st.rerun()

# ── Login Gate ────────────────────────────────────────────────────────────────
if not auth.is_logged_in():
    st.markdown("""
    <style>
    .login-box { max-width:420px; margin:60px auto; }
    </style>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.markdown("## 🎓 EduTrack AI")
        st.caption("Seu assistente acadêmico inteligente")
        st.markdown("---")

        tab_login, tab_signup = st.tabs(["Entrar", "Criar conta"])

        with tab_login:
            with st.form("form_login"):
                email = st.text_input("E-mail", placeholder="seu@email.com")
                senha = st.text_input("Senha", type="password")
                submitted = st.form_submit_button("Entrar", use_container_width=True)
                if submitted:
                    if not email or not senha:
                        st.error("Preencha e-mail e senha.")
                    else:
                        try:
                            auth.login(email, senha)
                            st.success("Login realizado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")

        with tab_signup:
            with st.form("form_signup"):
                nome = st.text_input("Nome completo")
                email2 = st.text_input("E-mail", placeholder="seu@email.com", key="su_email")
                senha2 = st.text_input("Senha", type="password", key="su_pass")
                senha3 = st.text_input("Confirmar senha", type="password")
                submitted2 = st.form_submit_button("Criar conta", use_container_width=True)
                if submitted2:
                    if not nome or not email2 or not senha2:
                        st.error("Preencha todos os campos.")
                    elif senha2 != senha3:
                        st.error("As senhas não coincidem.")
                    else:
                        try:
                            auth.signup(nome, email2, senha2)
                            st.success("Conta criada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")
    st.stop()


# ── Dashboard (autenticado) ───────────────────────────────────────────────────
user = auth.current_user()
st.title(f"👋 Olá, {user.get('name', 'Aluno')}!")
st.caption("Aqui está um resumo do seu progresso acadêmico.")

# Buscar dados reais
try:
    subjects_data = api.get("subjects", "/subjects")
    subjects = subjects_data.get("items", subjects_data) if isinstance(subjects_data, dict) else subjects_data
    if isinstance(subjects, dict):
        subjects = subjects.get("result", [])
except Exception:
    subjects = []

try:
    tasks_data = api.get("academic_tasks", "/academic_tasks")
    tasks = tasks_data.get("items", tasks_data) if isinstance(tasks_data, dict) else tasks_data
    if isinstance(tasks, dict):
        tasks = tasks.get("result", [])
except Exception:
    tasks = []

# Calcular métricas
today_str = date.today().isoformat()

def is_overdue(task):
    due = task.get("due_date", "")
    if not due:
        return False
    due_date = due[:10]
    return due_date < today_str and task.get("status", "") != "Concluída"

total_subjects  = len(subjects) if isinstance(subjects, list) else 0
total_tasks     = len(tasks) if isinstance(tasks, list) else 0
pending_tasks   = len([t for t in (tasks or []) if t.get("status") in ("Pendente", "Em andamento")])
overdue_tasks   = len([t for t in (tasks or []) if is_overdue(t)])
completed_tasks = len([t for t in (tasks or []) if t.get("status") == "Concluída"])
progress_pct    = round((completed_tasks / total_tasks * 100) if total_tasks else 0)

# ── Métricas ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("📚 Disciplinas", total_subjects)
c2.metric("📝 Tarefas Pendentes", pending_tasks)
c3.metric("⚠️ Em Atraso", overdue_tasks, delta=f"-{overdue_tasks}" if overdue_tasks else None,
          delta_color="inverse")
c4.metric("✅ Progresso Geral", f"{progress_pct}%")

st.markdown("---")

# ── Barra de progresso ────────────────────────────────────────────────────────
st.subheader("📊 Progresso das Tarefas")
st.progress(progress_pct / 100)
st.caption(f"{completed_tasks} de {total_tasks} tarefas concluídas")

st.markdown("---")

# ── Próximas tarefas ──────────────────────────────────────────────────────────
st.subheader("⏰ Próximas Tarefas")

if not tasks:
    st.info("🎉 Nenhuma tarefa cadastrada ainda. Acesse **Tarefas** no menu lateral para começar!")
else:
    upcoming = [
        t for t in tasks
        if t.get("status") != "Concluída" and t.get("due_date", "") >= today_str
    ]
    upcoming.sort(key=lambda t: t.get("due_date", "9999"))

    if not upcoming:
        st.success("✅ Não há tarefas pendentes com prazo futuro.")
    else:
        for task in upcoming[:5]:
            due = task.get("due_date", "")[:10]
            days_left = (date.fromisoformat(due) - date.today()).days if due else 0
            label = "🔴" if days_left <= 1 else ("🟡" if days_left <= 3 else "🟢")
            subj = task.get("subject_name", task.get("subject_id", "—"))
            with st.container(border=True):
                col_a, col_b = st.columns([3,1])
                col_a.markdown(f"{label} **{task.get('title','Sem título')}**  \n📚 {subj}")
                col_b.markdown(f"📅 `{due}`  \n_{days_left}d restantes_")

st.markdown("---")

# ── Estado vazio ──────────────────────────────────────────────────────────────
if total_subjects == 0 and total_tasks == 0:
    st.info("""
    ### 🚀 Comece agora!
    Você ainda não tem dados cadastrados. Use o menu lateral para:
    - **📚 Disciplinas** → Cadastre suas matérias
    - **📝 Tarefas** → Adicione suas tarefas e prazos
    """)

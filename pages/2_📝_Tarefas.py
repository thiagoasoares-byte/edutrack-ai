import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import utils.api  as api
import utils.auth as auth
from datetime import date, datetime

st.set_page_config(page_title="Tarefas", page_icon="📝", layout="wide")
auth.require_auth()

with st.sidebar:
    if st.button("🚪 Sair", use_container_width=True):
        auth.logout()
        st.rerun()

st.title("📝 Minhas Tarefas")

STATUS_OPTIONS   = ["Pendente", "Em andamento", "Concluída"]
PRIORITY_OPTIONS = ["Baixa", "Média", "Alta"]
PRIORITY_ICON    = {"Alta": "🔴", "Média": "🟡", "Baixa": "🟢"}

def load_subjects():
    try:
        data = api.get("subjects", "/subjects")
        items = data if isinstance(data, list) else data.get("items", data.get("result", []))
        return items
    except Exception:
        return []

def load_tasks(subject_id=None, status_filter=None):
    params = {}
    if subject_id:
        params["subject_id"] = subject_id
    if status_filter and status_filter != "Todas":
        params["status"] = status_filter
    try:
        data = api.get("academic_tasks", "/academic_tasks", params)
        return data if isinstance(data, list) else data.get("items", data.get("result", []))
    except Exception as e:
        st.error(f"Erro ao carregar tarefas: {e}")
        return []

subjects = load_subjects()
subj_map = {s["id"]: s.get("name","") for s in subjects}

tab_lista, tab_nova = st.tabs(["📋 Minhas Tarefas", "➕ Nova Tarefa"])

# ──────────────────────────── LISTA ──────────────────────────────────────────
with tab_lista:
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filtro_status = st.selectbox("Filtrar por Status", ["Todas"] + STATUS_OPTIONS)
    with fc2:
        subj_opts = {"Todas as disciplinas": None} | {s.get("name",""): s["id"] for s in subjects}
        filtro_subj_name = st.selectbox("Filtrar por Disciplina", list(subj_opts.keys()))
        filtro_subj_id   = subj_opts[filtro_subj_name]
    with fc3:
        search_task = st.text_input("🔍 Buscar tarefa", placeholder="Ex: Prova")

    tasks = load_tasks(filtro_subj_id, filtro_status)

    # Busca local por título
    if search_task:
        tasks = [t for t in tasks if search_task.lower() in t.get("title","").lower()]

    # Ordenar por prazo
    today_str = date.today().isoformat()
    tasks.sort(key=lambda t: t.get("due_date","9999")[:10])

    # Separar grupos
    overdue  = [t for t in tasks if t.get("status") != "Concluída"
                and (t.get("due_date","")[:10] or "9999") < today_str]
    pending  = [t for t in tasks if t.get("status") in ("Pendente","Em andamento")
                and (t.get("due_date","")[:10] or "9999") >= today_str]
    done     = [t for t in tasks if t.get("status") == "Concluída"]

    def render_task(task):
        tid      = task.get("id")
        status   = task.get("status","Pendente")
        due      = (task.get("due_date","")[:10]) or ""
        priority = task.get("priority","Média")
        picon    = PRIORITY_ICON.get(priority,"🟡")
        subj_nm  = subj_map.get(task.get("subject_id"), "—")
        is_over  = due < today_str if due else False
        due_color= "🔴" if (is_over and status != "Concluída") else "📅"

        with st.container(border=True):
            h1, h2 = st.columns([4,1])
            with h1:
                st.markdown(f"**{picon} {task.get('title','Sem título')}**")
                st.caption(f"📚 {subj_nm}  •  {due_color} {due}  •  Status: {status}")
                if task.get("description"):
                    st.markdown(f"_{task['description']}_")
            with h2:
                if status != "Concluída":
                    if st.button("✅ Concluir", key=f"done_{tid}", use_container_width=True):
                        try:
                            api.patch("academic_tasks", f"/academic_tasks/{tid}",
                                      {"status": "Concluída"})
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                if st.button("✏️ Editar", key=f"tedit_{tid}", use_container_width=True):
                    st.session_state[f"t_editing_{tid}"] = True
                if st.button("🗑️ Excluir", key=f"tdel_{tid}", use_container_width=True):
                    st.session_state[f"t_confirm_{tid}"] = True

            if st.session_state.get(f"t_confirm_{tid}"):
                st.warning(f"⚠️ Excluir **{task.get('title')}**?")
                cd1, cd2 = st.columns(2)
                if cd1.button("Confirmar", key=f"tcy_{tid}", type="primary"):
                    try:
                        api.delete("academic_tasks", f"/academic_tasks/{tid}")
                        st.success("Tarefa excluída.")
                        st.session_state.pop(f"t_confirm_{tid}", None)
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                if cd2.button("Cancelar", key=f"tcn_{tid}"):
                    st.session_state.pop(f"t_confirm_{tid}", None)
                    st.rerun()

            if st.session_state.get(f"t_editing_{tid}"):
                with st.form(f"form_tedit_{tid}"):
                    st.markdown("**Editar Tarefa**")
                    nt  = st.text_input("Título", value=task.get("title",""))
                    nd  = st.text_area("Descrição", value=task.get("description",""))
                    ndue = st.date_input("Prazo", value=datetime.strptime(due, "%Y-%m-%d").date() if due else date.today())
                    nst = st.selectbox("Status", STATUS_OPTIONS, index=STATUS_OPTIONS.index(status) if status in STATUS_OPTIONS else 0)
                    npr = st.selectbox("Prioridade", PRIORITY_OPTIONS, index=PRIORITY_OPTIONS.index(priority) if priority in PRIORITY_OPTIONS else 1)
                    nsid_name = st.selectbox("Disciplina", list(subj_map.values()),
                                             index=list(subj_map.keys()).index(task.get("subject_id")) if task.get("subject_id") in subj_map else 0)
                    nsid = [k for k,v in subj_map.items() if v == nsid_name]
                    nsid = nsid[0] if nsid else task.get("subject_id")
                    es1, es2 = st.columns(2)
                    sv = es1.form_submit_button("💾 Salvar", use_container_width=True)
                    cn = es2.form_submit_button("✖️ Cancelar", use_container_width=True)
                    if sv:
                        try:
                            api.patch("academic_tasks", f"/academic_tasks/{tid}", {
                                "title": nt, "description": nd,
                                "due_date": ndue.isoformat(), "status": nst,
                                "priority": npr, "subject_id": nsid,
                            })
                            st.success("Tarefa atualizada!")
                            st.session_state.pop(f"t_editing_{tid}", None)
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                    if cn:
                        st.session_state.pop(f"t_editing_{tid}", None)
                        st.rerun()

    if overdue:
        st.markdown("### 🔴 Em Atraso")
        for t in overdue:
            render_task(t)

    if pending:
        st.markdown("### 📌 Pendentes / Em Andamento")
        for t in pending:
            render_task(t)

    if done:
        with st.expander(f"✅ Concluídas ({len(done)})", expanded=False):
            for t in done:
                render_task(t)

    if not tasks:
        st.info("Nenhuma tarefa encontrada. Use a aba **Nova Tarefa** para adicionar.")

# ──────────────────────────── NOVA TAREFA ────────────────────────────────────
with tab_nova:
    if not subjects:
        st.warning("⚠️ Você precisa cadastrar pelo menos uma disciplina antes de adicionar tarefas.")
    else:
        with st.form("form_nova_tarefa"):
            st.subheader("Cadastrar Nova Tarefa")
            titulo    = st.text_input("Título *")
            descricao = st.text_area("Descrição")
            prazo     = st.date_input("Prazo *", value=date.today())
            prioridade= st.selectbox("Prioridade", PRIORITY_OPTIONS, index=1)
            status_new= st.selectbox("Status inicial", STATUS_OPTIONS[:2])
            subj_sel  = st.selectbox("Disciplina *", [s.get("name","") for s in subjects])
            subj_id   = next((s["id"] for s in subjects if s.get("name") == subj_sel), None)

            submitted = st.form_submit_button("💾 Cadastrar", use_container_width=True)
            if submitted:
                if not titulo or not subj_id:
                    st.error("Título e disciplina são obrigatórios.")
                else:
                    try:
                        api.post("academic_tasks", "/academic_tasks", {
                            "title": titulo,
                            "description": descricao,
                            "due_date": prazo.isoformat(),
                            "status": status_new,
                            "priority": prioridade,
                            "subject_id": subj_id,
                        })
                        st.success(f"✅ Tarefa **{titulo}** cadastrada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import utils.api  as api
import utils.auth as auth
from datetime import date

st.set_page_config(page_title="Disciplinas", page_icon="📚", layout="wide")
auth.require_auth()

# ── Sidebar logout ────────────────────────────────────────────────────────────
with st.sidebar:
    if st.button("🚪 Sair", use_container_width=True):
        auth.logout()
        st.rerun()

st.title("📚 Minhas Disciplinas")

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_subjects(search="", only_overdue=False):
    params = {}
    if search:
        params["name"] = search
    try:
        data = api.get("subjects", "/subjects", params)
        items = data if isinstance(data, list) else data.get("items", data.get("result", []))
    except Exception as e:
        st.error(f"Erro ao carregar disciplinas: {e}")
        return []
    if only_overdue:
        items = [s for s in items if s.get("has_overdue")]
    return items

def load_tasks_for_subject(subject_id):
    try:
        data = api.get("academic_tasks", "/academic_tasks", {"subject_id": subject_id})
        return data if isinstance(data, list) else data.get("items", data.get("result", []))
    except Exception:
        return []

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_lista, tab_nova = st.tabs(["📋 Minhas Disciplinas", "➕ Nova Disciplina"])

# ─────────────────────────── LISTA ───────────────────────────────────────────
with tab_lista:
    col_search, col_filter = st.columns([3,1])
    with col_search:
        search = st.text_input("🔍 Buscar por nome", placeholder="Ex: Cálculo")
    with col_filter:
        only_overdue = st.checkbox("⚠️ Apenas com atraso")

    subjects = load_subjects(search, only_overdue)

    if not subjects:
        st.info("Nenhuma disciplina encontrada. Cadastre uma na aba **Nova Disciplina**.")
    else:
        st.caption(f"{len(subjects)} disciplina(s) encontrada(s)")
        for subj in subjects:
            sid = subj.get("id")
            # Calcular progresso por disciplina via tasks
            tasks = load_tasks_for_subject(sid)
            total_t = len(tasks)
            done_t  = len([t for t in tasks if t.get("status") == "Concluída"])
            prog    = int((done_t / total_t * 100)) if total_t else 0
            today   = date.today().isoformat()
            overdue = [t for t in tasks if t.get("status") != "Concluída"
                       and (t.get("due_date","")[:10] or "9999") < today]

            with st.container(border=True):
                hcol1, hcol2 = st.columns([4,1])
                with hcol1:
                    badge = " 🔴" if overdue else ""
                    st.markdown(f"### {subj.get('name','')}{badge}")
                    st.caption(f"👨‍🏫 {subj.get('teacher','—')}  •  📝 {total_t} tarefa(s)  •  Semestre: {subj.get('semester','—')}")
                    if total_t:
                        st.progress(prog / 100, text=f"{prog}% concluído")
                    if overdue:
                        st.warning(f"⚠️ {len(overdue)} tarefa(s) em atraso nesta disciplina")

                with hcol2:
                    # Edit & Delete com confirmação
                    if st.button("✏️ Editar", key=f"edit_{sid}", use_container_width=True):
                        st.session_state[f"editing_{sid}"] = True
                    if st.button("🗑️ Excluir", key=f"del_{sid}", use_container_width=True):
                        st.session_state[f"confirm_del_{sid}"] = True

                # ── Confirmar exclusão ─────────────────────────────────────
                if st.session_state.get(f"confirm_del_{sid}"):
                    st.warning(f"⚠️ Tem certeza que quer excluir **{subj.get('name')}**? Esta ação não pode ser desfeita.")
                    cc1, cc2 = st.columns(2)
                    if cc1.button("Sim, excluir", key=f"conf_yes_{sid}", type="primary"):
                        try:
                            api.delete("subjects", f"/subjects/{sid}")
                            st.success("Disciplina excluída.")
                            st.session_state.pop(f"confirm_del_{sid}", None)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")
                    if cc2.button("Cancelar", key=f"conf_no_{sid}"):
                        st.session_state.pop(f"confirm_del_{sid}", None)
                        st.rerun()

                # ── Formulário de edição inline ───────────────────────────
                if st.session_state.get(f"editing_{sid}"):
                    with st.form(f"form_edit_{sid}"):
                        st.markdown("**Editar Disciplina**")
                        new_name    = st.text_input("Nome",       value=subj.get("name",""))
                        new_teacher = st.text_input("Professor",  value=subj.get("teacher",""))
                        new_sem     = st.text_input("Semestre",   value=subj.get("semester",""),
                                                    placeholder="Ex: 2026/1")
                        new_desc    = st.text_area("Descrição",   value=subj.get("description",""))
                        ec1, ec2 = st.columns(2)
                        save   = ec1.form_submit_button("💾 Salvar",   use_container_width=True)
                        cancel = ec2.form_submit_button("✖️ Cancelar", use_container_width=True)
                        if save:
                            try:
                                api.patch("subjects", f"/subjects/{sid}", {
                                    "name": new_name, "teacher": new_teacher,
                                    "semester": new_sem, "description": new_desc,
                                })
                                st.success("Disciplina atualizada!")
                                st.session_state.pop(f"editing_{sid}", None)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro: {e}")
                        if cancel:
                            st.session_state.pop(f"editing_{sid}", None)
                            st.rerun()

# ─────────────────────────── NOVA DISCIPLINA ─────────────────────────────────
with tab_nova:
    with st.form("form_nova_disciplina"):
        st.subheader("Cadastrar Nova Disciplina")
        nome     = st.text_input("Nome da Disciplina *")
        professor= st.text_input("Professor(a) *")
        semestre = st.text_input("Semestre", placeholder="Ex: 2026/1")
        descricao= st.text_area("Descrição", placeholder="Opcional")
        submitted= st.form_submit_button("💾 Cadastrar", use_container_width=True)

        if submitted:
            if not nome or not professor:
                st.error("Nome e professor são obrigatórios.")
            else:
                try:
                    api.post("subjects", "/subjects", {
                        "name": nome, "teacher": professor,
                        "semester": semestre, "description": descricao,
                    })
                    st.success(f"✅ Disciplina **{nome}** cadastrada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")

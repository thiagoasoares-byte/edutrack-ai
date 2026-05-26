import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import utils.api  as api
import utils.auth as auth
from datetime import date
import json, io

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide")
auth.require_auth()

with st.sidebar:
    if st.button("🚪 Sair", use_container_width=True):
        auth.logout()
        st.rerun()

st.title("📊 Relatórios e Progresso")

# ── Carregar dados ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def fetch_all(token):
    try:
        sd = api.get("subject", "/list")
        subjs = sd if isinstance(sd, list) else sd.get("items", sd.get("result", []))
    except Exception:
        subjs = []
    try:
        td = api.get("academic_tasks", "/list")
        tasks = td if isinstance(td, list) else td.get("items", td.get("result", []))
    except Exception:
        tasks = []
    return subjs, tasks

token = st.session_state.get("auth_token","")
subjects, tasks = fetch_all(token)

today = date.today().isoformat()
subj_map = {s["id"]: s.get("name","") for s in subjects}

# ── Métricas Gerais ────────────────────────────────────────────────────────────
st.subheader("📈 Visão Geral")
total_s  = len(subjects)
total_t  = len(tasks)
done_t   = len([t for t in tasks if t.get("status") == "Concluída"])
pend_t   = len([t for t in tasks if t.get("status") in ("Pendente","Em andamento")])
over_t   = len([t for t in tasks if t.get("status") != "Concluída"
                and (t.get("due_date","")[:10] or "9999") < today])
prog     = round(done_t / total_t * 100) if total_t else 0

c1,c2,c3,c4 = st.columns(4)
c1.metric("📚 Disciplinas", total_s)
c2.metric("✅ Concluídas", done_t)
c3.metric("⏳ Pendentes",   pend_t)
c4.metric("⚠️ Em atraso",   over_t)
st.progress(prog / 100, text=f"Progresso geral: {prog}%")

st.markdown("---")

# ── Progresso por disciplina ───────────────────────────────────────────────────
st.subheader("📚 Progresso por Disciplina")
if not subjects:
    st.info("Nenhuma disciplina cadastrada.")
else:
    for subj in subjects:
        sid   = subj["id"]
        stasks= [t for t in tasks if t.get("subject_id") == sid]
        tot   = len(stasks)
        done  = len([t for t in stasks if t.get("status") == "Concluída"])
        over  = len([t for t in stasks if t.get("status") != "Concluída"
                     and (t.get("due_date","")[:10] or "9999") < today])
        p     = int(done / tot * 100) if tot else 0
        with st.container(border=True):
            sc1, sc2 = st.columns([3,1])
            sc1.markdown(f"**{subj.get('name','')}**  •  👨‍🏫 {subj.get('teacher','—')}  •  Sem: {subj.get('semester','—')}")
            sc1.progress(p / 100, text=f"{p}%  ({done}/{tot} tarefas)")
            if over:
                sc1.warning(f"⚠️ {over} em atraso")
            sc2.metric("Tarefas", tot)

st.markdown("---")

# ── Histórico de tarefas ───────────────────────────────────────────────────────
st.subheader("📋 Histórico de Tarefas")

filter_s = st.selectbox("Filtrar por status", ["Todas","Pendente","Em andamento","Concluída"])
filtered = tasks if filter_s == "Todas" else [t for t in tasks if t.get("status") == filter_s]

if filtered:
    rows = []
    for t in sorted(filtered, key=lambda x: x.get("due_date","9999")[:10]):
        rows.append({
            "Título":      t.get("title",""),
            "Disciplina":  subj_map.get(t.get("subject_id"), "—"),
            "Prazo":       (t.get("due_date","")[:10]) or "—",
            "Status":      t.get("status","—"),
            "Prioridade":  t.get("priority","—"),
        })
    st.dataframe(rows, use_container_width=True)
else:
    st.info("Nenhuma tarefa encontrada.")

st.markdown("---")

# ── Exportar ───────────────────────────────────────────────────────────────────
st.subheader("⬇️ Exportar Dados")
ec1, ec2 = st.columns(2)

# CSV
if ec1.button("📄 Exportar Tarefas em CSV", use_container_width=True):
    lines = ["Título,Disciplina,Prazo,Status,Prioridade"]
    for t in tasks:
        lines.append(",".join([
            f'"{t.get("title","")}"',
            f'"{subj_map.get(t.get("subject_id"),"—")}"',
            f'"{(t.get("due_date","")[:10]) or ""}"',
            f'"{t.get("status","")}"',
            f'"{t.get("priority","")}"',
        ]))
    csv_bytes = "\n".join(lines).encode("utf-8")
    st.download_button("⬇️ Baixar CSV", csv_bytes, "tarefas_edutrack.csv", "text/csv",
                       key="dl_csv")

# JSON
if ec2.button("🗂️ Exportar Dados Completos (JSON)", use_container_width=True):
    export = {"subjects": subjects, "tasks": tasks}
    json_bytes = json.dumps(export, ensure_ascii=False, indent=2).encode("utf-8")
    st.download_button("⬇️ Baixar JSON", json_bytes, "edutrack_backup.json", "application/json",
                       key="dl_json")

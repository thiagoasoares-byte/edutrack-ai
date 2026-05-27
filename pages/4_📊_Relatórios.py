import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import utils.api  as api
import utils.auth as auth
from datetime import date
import json, io


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_pdf_report(rows, title="Relatório de Tarefas"):
    # Produz um PDF simples em bytes sem dependências externas.
    content_lines = []
    content_lines.append(f"BT /F1 16 Tf 50 760 Td ({_pdf_escape(title)}) Tj ET")
    y = 740
    for row in rows:
        if y < 60:
            break
        content_lines.append(f"BT /F1 10 Tf 50 {y} Td ({_pdf_escape(row)}) Tj ET")
        y -= 14

    stream = "\n".join(content_lines).encode("latin1")
    length = len(stream)

    objects = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj")
    objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj")
    objects.append(b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj")
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj")
    objects.append(b"5 0 obj << /Length " + str(length).encode("utf-8") + b" >> stream\n" + stream + b"\nendstream endobj")

    pdf_body = [b"%PDF-1.4"]
    offsets = []
    pos = len(pdf_body[0]) + 1
    for obj in objects:
        offsets.append(pos)
        pdf_body.append(obj)
        pos += len(obj) + 1

    xref = [b"xref", f"0 {len(objects) + 1}".encode("utf-8"), b"0000000000 65535 f "]
    for off in offsets:
        xref.append(f"{off:010d} 00000 n ".encode("utf-8"))

    startxref = pos + sum(len(x) + 1 for x in xref)
    trailer = [b"trailer << /Size " + str(len(objects) + 1).encode("utf-8") + b" /Root 1 0 R >>", b"startxref " + str(startxref).encode("utf-8"), b"%%EOF"]
    pdf_bytes = b"\n".join(pdf_body + xref + trailer)
    return pdf_bytes

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
rows = []

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
ec1, ec2, ec3 = st.columns(3)

with ec1:
    if st.button("📄 Exportar Tarefas em CSV", use_container_width=True, key="btn_csv_export"):
        lines = ["Título,Disciplina,Prazo,Status,Prioridade"]
        for row in rows:
            lines.append(",".join([
                f'"{row["Título"]}"',
                f'"{row["Disciplina"]}"',
                f'"{row["Prazo"]}"',
                f'"{row["Status"]}"',
                f'"{row["Prioridade"]}"',
            ]))
        csv_bytes = "\n".join(lines).encode("utf-8")
        st.download_button("⬇️ Baixar CSV", csv_bytes, "tarefas_edutrack.csv", "text/csv",
                           key="dl_csv")

with ec2:
    if st.button("📄 Exportar Tarefas em PDF", use_container_width=True, key="btn_pdf_export"):
        pdf_rows = [
            f"{row['Título']} | {row['Disciplina']} | {row['Prazo']} | {row['Status']} | {row['Prioridade']}"
            for row in rows
        ]
        pdf_bytes = generate_pdf_report(pdf_rows, title="Relatório de Tarefas")
        st.download_button("⬇️ Baixar PDF", pdf_bytes, "tarefas_edutrack.pdf", "application/pdf",
                           key="dl_pdf")

with ec3:
    if st.button("🗂️ Exportar Dados Completos (JSON)", use_container_width=True, key="btn_json_export"):
        export = {"subjects": subjects, "tasks": filtered}
        json_bytes = json.dumps(export, ensure_ascii=False, indent=2).encode("utf-8")
        st.download_button("⬇️ Baixar JSON", json_bytes, "edutrack_backup.json", "application/json",
                           key="dl_json")

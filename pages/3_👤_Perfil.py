import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import utils.api  as api
import utils.auth as auth
import utils.ui as ui

ui.apply_theme(page_title="Perfil", page_icon="👤", layout="centered")
auth.require_auth()

with st.sidebar:
    if st.button("🚪 Sair", use_container_width=True):
        auth.logout()
        st.rerun()

st.title("👤 Meu Perfil")

user = auth.current_user()

col1, col2 = st.columns([1,3])
with col1:
    seed = (user.get("name","User")).replace(" ", "%20")
    st.image(f"https://api.dicebear.com/8.x/initials/svg?seed={seed}", width=120)
with col2:
    st.markdown(f"### {user.get('name','—')}")
    st.caption(f"📧 {user.get('email','—')}")

st.markdown("---")

# ── Editar perfil ─────────────────────────────────────────────────────────────
st.subheader("✏️ Editar Informações")
with st.form("form_perfil"):
    new_name  = st.text_input("Nome",  value=user.get("name",""))
    new_email = st.text_input("Email", value=user.get("email",""))
    submitted = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)

    if submitted:
        payload = {}
        if new_name  and new_name  != user.get("name"):  payload["name"]  = new_name
        if new_email and new_email != user.get("email"): payload["email"] = new_email
        if not payload:
            st.info("Nenhuma alteração detectada.")
        else:
            try:
                resp = api.patch("auth", "/update_profile", payload)
                updated = resp.get("user", resp)
                st.session_state["user"] = updated
                st.success("✅ Perfil atualizado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

st.markdown("---")

# ── Redefinir senha via e-mail (dentro da seção perfil)
st.subheader("🔑 Redefinir Senha por E-mail")
st.caption("Enviaremos um link de redefinição para o seu e-mail cadastrado.")

if 'profile_reset_step' not in st.session_state:
    st.session_state.profile_reset_step = 'request'

if st.session_state.profile_reset_step == 'request':
    with st.form("form_reset"):
        reset_email = st.text_input("E-mail", value=user.get("email",""), disabled=True)
        send = st.form_submit_button("📧 Enviar código de recuperação", use_container_width=True)
        if send:
            try:
                api.post("auth", "/forgot_password", {"email": reset_email})
                st.success("Se o e-mail existir, você receberá instruções em breve.")
                st.session_state.profile_reset_step = 'reset'
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao enviar link: {e}")

elif st.session_state.profile_reset_step == 'reset':
    st.info("Verifique seu e-mail para obter o código de recuperação.")
    with st.form("form_reset_confirm"):
        token = st.text_input("Código (Token)", help="Cole o código recebido por e-mail")
        new_password = st.text_input("Nova Senha", type="password")
        confirm_password = st.text_input("Confirme a Nova Senha", type="password")

        col1, col2 = st.columns(2)
        with col1:
            confirm = st.form_submit_button("Redefinir Senha", use_container_width=True)
            if confirm:
                if new_password != confirm_password:
                    st.error("As senhas não coincidem.")
                elif len(new_password) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres.")
                else:
                    try:
                        api.post("auth", "/reset_password", {"token": token, "new_password": new_password})
                        st.success("Senha redefinida com sucesso! Você já pode fazer login.")
                        st.session_state.profile_reset_step = 'request'
                        st.rerun()
                    except Exception as e:
                        st.error(f"Falha: {e}")
        with col2:
            if st.form_submit_button("Voltar", use_container_width=True):
                st.session_state.profile_reset_step = 'request'
                st.rerun()

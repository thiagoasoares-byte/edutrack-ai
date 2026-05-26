import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import utils.api  as api
import utils.auth as auth

st.set_page_config(page_title="Perfil", page_icon="👤", layout="centered")
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
    st.markdown("**Alterar senha** _(deixe em branco para não alterar)_")
    new_pass  = st.text_input("Nova senha",         type="password")
    new_pass2 = st.text_input("Confirmar nova senha", type="password")
    submitted = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)

    if submitted:
        if new_pass and new_pass != new_pass2:
            st.error("As senhas não coincidem.")
        else:
            payload = {}
            if new_name  and new_name  != user.get("name"):  payload["name"]  = new_name
            if new_email and new_email != user.get("email"): payload["email"] = new_email
            if new_pass:                                       payload["password"] = new_pass

            if not payload:
                st.info("Nenhuma alteração detectada.")
            else:
                try:
                    resp = api.patch("auth", "/auth/me", payload)
                    updated = resp.get("user", resp)
                    st.session_state["user"] = updated
                    st.success("✅ Perfil atualizado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")

st.markdown("---")

# ── Redefinir senha via e-mail ─────────────────────────────────────────────────
st.subheader("🔑 Redefinir Senha por E-mail")
st.caption("Enviaremos um link de redefinição para o seu e-mail cadastrado.")
with st.form("form_reset"):
    reset_email = st.text_input("E-mail", value=user.get("email",""), disabled=True)
    send = st.form_submit_button("📧 Enviar link de redefinição")
    if send:
        try:
            api.post("auth", "/auth/forgot-password", {"email": reset_email})
            st.success("E-mail enviado! Verifique sua caixa de entrada.")
        except Exception as e:
            st.error(f"Erro: {e}")

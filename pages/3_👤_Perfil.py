import streamlit as st

# 1. Set page config
st.set_page_config(page_title="Meu Perfil", page_icon="👤")

# 2. Add a title
st.title("Meu Perfil")

# 3. Simulate user data (em breve, virá do Xano)
# Em um aplicativo real, você obteria esses dados do usuário logado
user_data = {
    "name": "Aluno impacta",
    "email": "aluno@impacta.com.br",
    "universidade": "Impacta" 
}

# 4. Display current user info
st.subheader("Informações Atuais")
col1, col2 = st.columns(2)
with col1:
    st.image("https://api.dicebear.com/8.x/initials/svg?seed=Aluno%20impacta", width=150)
with col2:
    st.write(f"**Nome:** {user_data['name']}")
    st.write(f"**Email:** {user_data['email']}")
    st.write(f"**Universidade:** {user_data['universidade']}")

st.markdown("---")

# 5. Create an "Edit Profile" form
st.subheader("Editar Perfil")
with st.form("edit_profile_form"):
    st.write("Atualize suas informações abaixo:")
    
    # 6. Add input fields
    new_name = st.text_input("Nome", value=user_data["name"])
    new_email = st.text_input("Email", value=user_data["email"])
    new_universidade = st.text_input("Universidade", value=user_data["universidade"])
    
    # 7. Add a submit button
    submitted = st.form_submit_button("Salvar Alterações")
    
    # 8. Handle form submission
    if submitted:
        # Aqui você atualizaria os dados no banco de dados
        # Por enquanto, apenas exibimos uma mensagem de sucesso
        st.success("Perfil atualizado com sucesso! (Simulação)")

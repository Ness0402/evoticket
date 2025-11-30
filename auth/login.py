import streamlit as st
from auth.user_service import get_user
from dotenv import load_dotenv

load_dotenv()

def login_ui():
    st.subheader("Acceso Administrativo")

    username_input = st.text_input("Usuario")
    password_input = st.text_input("Contraseña", type="password")

    login_btn = st.button("Ingresar")

    if login_btn:
        user = get_user(username_input)

        if not user:
            st.error("Usuario no encontrado")
            return False

        if not user.active:
            st.error("Usuario desactivado")
            return False

        if user.verify_password(password_input):
            st.session_state["user"] = user.username
            st.session_state["role"] = user.role
            st.success(f"Bienvenido, {user.name}")
            return True
        else:
            st.error("Contraseña incorrecta")
            return False

    return False

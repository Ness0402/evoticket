import streamlit as st
from auth.login import login_ui
from auth.roles import require_role
from admin.eventos import admin_eventos_ui
from admin.tickets import admin_tickets_ui
from admin.categoriatickets import admin_ticket_categories_ui
from admin.users import admin_users_ui
from admin.compra import admin_compras_ui
from public.eventos import public_eventos_ui
from public.compra import compra_tickets_ui
import uuid

st.set_page_config(
    page_title="Evoticket",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "view" not in st.session_state:
    st.session_state.view = "public"

if "user" not in st.session_state:
    st.session_state.user = None

st.sidebar.title("Menú")

if st.session_state.user is None:
    menu = st.sidebar.selectbox(
        "Opciones",
        ["Eventos Públicos", "Iniciar sesión"]
    )

    if menu == "Eventos Públicos":
        public_eventos_ui()
        st.stop()

    elif menu == "Iniciar sesión":
        login_success = login_ui()
        if login_success:
            st.session_state.view = "private"
            st.rerun()

else:
    menu = st.sidebar.selectbox(
        "Opciones",
        [
            "Eventos Públicos",
            "Gestión Eventos",
            "Gestión Tickets Categoría",
            "Gestión Tickets",
            "Gestión Usuarios",
            "Gestión Compras",
            "Cerrar sesión"
        ]
    )

    if menu == "Eventos Públicos":
        public_eventos_ui()

    elif menu == "Gestión Eventos":
        admin_eventos_ui()

    elif menu == "Gestión Tickets Categoría":
        admin_ticket_categories_ui()

    elif menu == "Gestión Tickets":
        admin_tickets_ui()

    elif menu == "Gestión Compras":
        admin_compras_ui()
    
    elif menu == "Gestión Usuarios":
        admin_users_ui()

    elif menu == "Cerrar sesión":
        st.session_state.clear()
        st.session_state.view = "public"
        st.rerun()

import streamlit as st
from database.connection import SessionLocal
from database.models import Evento
from public.compra import compra_tickets_ui
import uuid

db = SessionLocal()

def public_eventos_ui():
    if "vista" not in st.session_state:
        st.session_state["vista"] = "public"
    if "evento_compra_id" not in st.session_state:
        st.session_state["evento_compra_id"] = None
    if "compra_form_id" not in st.session_state:
        st.session_state["compra_form_id"] = str(uuid.uuid4())

    if st.session_state["vista"] == "public":
        st.title("🎉 Eventos Disponibles")
        eventos = db.query(Evento).all()

        for e in eventos:
            st.subheader(e.nombre)
            st.write(e.descripcion)
            st.write(f"📅 Fecha: {e.fecha}")

            if st.button(f"Comprar tickets - {e.id}", key=f"compra_{e.id}"):
                st.session_state["evento_compra_id"] = e.id
                st.session_state["vista"] = "compra"
                st.session_state["compra_form_id"] = str(uuid.uuid4())  # ID único por compra
                st.rerun()

    elif st.session_state["vista"] == "compra":
        if st.session_state["evento_compra_id"] is None:
            st.error("Evento no seleccionado.")
            return

        if st.button("⬅️ Volver a eventos"):
            st.session_state["vista"] = "public"
            st.session_state["evento_compra_id"] = None
            st.rerun()

        compra_tickets_ui(form_id=st.session_state["compra_form_id"])
import streamlit as st
from database.connection import SessionLocal
from database.models import Evento

db = SessionLocal()

def public_eventos_ui():
    st.title("🎉 Eventos Disponibles")
    eventos = db.query(Evento).all()

    for e in eventos:
        st.subheader(e.nombre)
        st.write(e.descripcion)
        st.write(f"📅 Fecha: {e.fecha}")

        if st.button(f"Comprar tickets - {e.nombre}", key=f"compra_{e.id}"):
            st.session_state["evento_compra_id"] = e.id
            st.session_state["vista"] = "compra"
            st.rerun()

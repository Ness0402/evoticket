import streamlit as st
from database.connection import SessionLocal
from database.models import Evento
from auth.roles import require_role
from sqlalchemy import asc, desc
import time

db = SessionLocal()

@require_role(["Administrador"])
def admin_eventos_ui():
    st.title("💥Gestión de Eventos")

    with st.popover("➕ Nuevo evento"):
        st.subheader("Crear evento")

        nombre = st.text_input("Nombre del evento", key="nuevo_nombre")
        descripcion = st.text_area("Descripción", key="nuevo_desc")
        fecha = st.date_input("Fecha", key="nuevo_fecha")

        if st.button("Guardar Evento", key="guardar_nuevo"):
            nuevo = Evento(nombre=nombre, descripcion=descripcion, fecha=fecha)
            db.add(nuevo)
            db.commit()
            st.success("Evento guardado")
            time.sleep(1)
            st.rerun()

    st.write("---")

    st.subheader("📋 Lista de eventos")

    eventos_query = db.query(Evento).order_by(Evento.id.desc())

    per_page = st.selectbox("Eventos por página", [5, 10, 20, 50], index=1)
    total = eventos_query.count()

    if "page_evt" not in st.session_state:
        st.session_state.page_evt = 1

    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        if st.button("⬅️ Prev") and st.session_state.page_evt > 1:
            st.session_state.page_evt -= 1
    with col2:
        if st.button("Next ➡️") and (st.session_state.page_evt * per_page) < total:
            st.session_state.page_evt += 1

    offset = (st.session_state.page_evt - 1) * per_page
    eventos = eventos_query.offset(offset).limit(per_page).all()

    st.write(f"Página {st.session_state.page_evt} / {(total // per_page) + 1}")

    for e in eventos:
        with st.expander(f"📌 {e.nombre} — {e.fecha}"):
            st.write(f"**Descripción:** {e.descripcion}")

            nuevo_nombre = st.text_input(f"Editar nombre {e.id}", e.nombre, key=f"nom_{e.id}")
            nueva_desc = st.text_area(f"Editar desc {e.id}", e.descripcion, key=f"desc_{e.id}")
            nueva_fecha = st.date_input(f"Editar fecha {e.id}", e.fecha, key=f"fec_{e.id}")

            colA, colB = st.columns(2)
            with colA:
                if st.button("💾 Guardar cambios", key=f"save_{e.id}"):
                    e.nombre = nuevo_nombre
                    e.descripcion = nueva_desc
                    e.fecha = nueva_fecha
                    db.commit()
                    st.success("Evento actualizado")
                    time.sleep(1)
                    st.rerun()

            with colB:
                if st.button("🗑️ Eliminar", key=f"del_{e.id}"):
                    db.delete(e)
                    db.commit()
                    st.warning("Evento eliminado")
                    time.sleep(1)
                    st.rerun()

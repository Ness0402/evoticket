import streamlit as st
from database.connection import SessionLocal
from database.models import TicketCategory
from auth.roles import require_role
import time

db = SessionLocal()

@require_role(["Administrador"])
def admin_ticket_categories_ui():
    st.title("🛠️Gestión de categorías de Tickets")
    with st.popover("➕ Nueva categoría"):
        st.subheader("Crear categoría")

        nombre = st.text_input("Nombre (ej: VIP, General)", key="cat_nombre")
        descripcion = st.text_area("Descripción", key="cat_desc")

        if st.button("Guardar categoría", key="save_cat"):
            cat = TicketCategory(nombre=nombre, descripcion=descripcion)
            db.add(cat)
            db.commit()
            st.success("Categoría creada")
            time.sleep(1)
            st.rerun()

    st.write("---")

    st.subheader("📋 Tabla de categoría de tickets")

    categorias_query = db.query(TicketCategory).order_by(TicketCategory.id.desc())

    per_page = st.selectbox("Categorías por página", [5, 10, 20, 50], index=1)
    total = categorias_query.count()

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
    categorias = categorias_query.offset(offset).limit(per_page).all()

    st.write(f"Página {st.session_state.page_evt} / {(total // per_page) + 1}")

    categorias = db.query(TicketCategory).order_by(TicketCategory.id.desc()).all()

    for c in categorias:
        with st.expander(f"🏷️ {c.nombre}"):
            new_nombre = st.text_input("Nombre", c.nombre, key=f"cat_nom_{c.id}")
            new_desc = st.text_area("Descripción", c.descripcion, key=f"cat_des_{c.id}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Guardar cambios", key=f"save_cat_{c.id}"):
                    c.nombre = new_nombre
                    c.descripcion = new_desc
                    db.commit()
                    st.success("Actualizado")
                    time.sleep(1)
                    st.rerun()

            with col2:
                if st.button("🗑️ Eliminar", key=f"del_cat_{c.id}"):
                    db.delete(c)
                    db.commit()
                    st.warning("Eliminado")
                    time.sleep(1)
                    st.rerun()

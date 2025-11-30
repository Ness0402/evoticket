import streamlit as st
from database.connection import SessionLocal
from database.models import TicketType, TicketCategory, Evento
from auth.roles import require_role
import time

db = SessionLocal()

@require_role(["Administrador", "Gestor de contenido"])
def admin_tickets_ui():
    st.title("🎟️Gestión de Tickets")

    eventos = db.query(Evento).all()
    categorias = db.query(TicketCategory).all()

    opciones_evento = {e.nombre: e.id for e in eventos}
    opciones_categoria = {c.nombre: c.id for c in categorias}

    with st.popover("➕ Nuevo ticket"):
        st.subheader("Agregar ticket")

        evento_id = st.selectbox(
            "Evento",
            list(opciones_evento.values()),
            format_func=lambda x: [k for k,v in opciones_evento.items() if v == x][0]
        )

        category_id = st.selectbox(
            "Categoría",
            list(opciones_categoria.values()),
            format_func=lambda x: [k for k,v in opciones_categoria.items() if v == x][0]
        )

        precio = st.number_input("Precio", min_value=0.0)
        cantidad_disponible = st.number_input("Cantidad disponible", min_value=0)

        if st.button("Guardar Ticket", key="guardar_ticket"):
            t = TicketType(
                evento_id=evento_id,
                category_id=category_id,
                precio=precio,
                cantidad_disponible=cantidad_disponible
            )
            db.add(t)
            db.commit()
            st.success("Ticket agregado")
            time.sleep(1)
            st.rerun()

    st.write("---")
    st.subheader("🎟️ Tabla de tickets")

    tickets_query = db.query(TicketType).order_by(TicketType.id.desc())
    per_page = st.selectbox("Tickets por página", [5, 10, 20, 50], index=1)
    total = tickets_query.count()

    if "page_tk" not in st.session_state:
        st.session_state.page_tk = 1

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Prev") and st.session_state.page_tk > 1:
        st.session_state.page_tk -= 1
    if col2.button("Next ➡️") and (st.session_state.page_tk * per_page) < total:
        st.session_state.page_tk += 1

    offset = (st.session_state.page_tk - 1) * per_page
    tickets = tickets_query.offset(offset).limit(per_page).all()

    st.subheader("🎟️ Tickets agrupados por evento")

    eventos_con_tickets = (
        db.query(Evento)
        .join(TicketType, TicketType.evento_id == Evento.id)
        .all()
    )

    for evento in eventos_con_tickets:
        with st.expander(f"📌 {evento.nombre}"):
            tickets_evento = (
                db.query(TicketType)
                .filter(TicketType.evento_id == evento.id)
                .all()
            )

            total_disponibles = sum(t.cantidad_disponible for t in tickets_evento)
            st.write(f"🟢 **Total disponibles: {total_disponibles}**")

            for t in tickets:
                evento_nombre = [k for k,v in opciones_evento.items() if v == t.evento_id][0]
                categoria_nombre = [k for k,v in opciones_categoria.items() if v == t.category_id][0]

                with st.expander(f"🎫 {categoria_nombre} - {evento_nombre} - ${t.precio}"):

                    new_category = st.selectbox(
                        f"Categoría {t.id}",
                        list(opciones_categoria.values()),
                        index=list(opciones_categoria.values()).index(t.category_id),
                        key=f"cat_{t.id}",
                        format_func=lambda x: [k for k,v in opciones_categoria.items() if v == x][0]
                    )

                    new_precio = st.number_input("Precio", value=t.precio, key=f"pre_{t.id}")
                    new_qty = st.number_input("Cantidad disponible", value=t.cantidad_disponible, key=f"qty_{t.id}")

                    colA, colB = st.columns(2)
                    with colA:
                        if st.button("💾 Guardar", key=f"save_tk_{t.id}"):
                            t.category_id = new_category
                            t.precio = new_precio
                            t.cantidad_disponible = new_qty
                            db.commit()
                            st.success("Actualizado")
                            time.sleep(1)
                            st.rerun()

                    with colB:
                        if st.button("🗑️ Eliminar", key=f"del_tk_{t.id}"):
                            db.delete(t)
                            db.commit()
                            st.warning("Eliminado")
                            time.sleep(1)
                            st.rerun()

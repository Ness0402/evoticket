import streamlit as st
from database.connection import SessionLocal
from database.models import Compra, Evento
from auth.roles import require_role
from utils.pdf_service import generar_pdf_ticket
from utils.qr_services import generar_qr
import time

db = SessionLocal()

@require_role(["Administrador", "Gestor de contenido"])
def admin_compras_ui():
    st.title("🛒 Gestión de Compras")

    eventos = db.query(Evento).order_by(Evento.fecha.desc()).all()
    opciones_evento = {e.nombre: e.id for e in eventos}

    filtro_evento = st.selectbox(
        "Filtrar por evento",
        ["Todos"] + list(opciones_evento.keys())
    )

    compras_query = db.query(Compra).order_by(Compra.fecha_compra.desc())

    if filtro_evento != "Todos":
        evento_id = opciones_evento[filtro_evento]
        compras_query = compras_query.filter(Compra.evento_id == evento_id)

    compras = compras_query.all()

    if not compras:
        st.info("No hay compras registradas.")
        return

    per_page = st.selectbox("Compras por página", [5, 10, 20, 50], index=1)
    total = len(compras)

    if "page_cp" not in st.session_state:
        st.session_state.page_cp = 1

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Prev") and st.session_state.page_cp > 1:
        st.session_state.page_cp -= 1
    if col2.button("Next ➡️") and (st.session_state.page_cp * per_page) < total:
        st.session_state.page_cp += 1

    offset = (st.session_state.page_cp - 1) * per_page
    compras_page = compras[offset: offset + per_page]

    for c in compras_page:
        evento_nombre = c.evento.nombre if c.evento else "Evento eliminado"

        with st.expander(f"🧾 {c.nombres} {c.apellidos} - {evento_nombre} - {c.cantidad} tickets"):

            st.write(f"📅 Fecha de compra: {c.fecha_compra}")
            st.write(f"📝 Documento: {c.tipo_documento} - {c.documento}")
            st.write(f"📧 Correo: {c.correo}")
            st.write(f"🎫 Cantidad: {c.cantidad}")

            qr_bytes = generar_qr(c.qr_uuid)
            pdf_bytes = generar_pdf_ticket(c, c.evento, qr_bytes)

            st.download_button(
                label="📄 Descargar Tickets en PDF",
                data=pdf_bytes,
                file_name=f"ticket_{c.id}.pdf",
                mime="application/pdf"
            )

            del_key = f"del_cp_{c.id}"
            confirm_key = f"confirm_del_{c.id}"

            if del_key not in st.session_state:
                st.session_state[del_key] = False
            if confirm_key not in st.session_state:
                st.session_state[confirm_key] = False

            if st.button(f"🗑️ Eliminar compra {c.id}", key=f"btn_{del_key}"):
                st.session_state[del_key] = True

            if st.session_state[del_key]:
                st.session_state[confirm_key] = st.checkbox(
                    "Confirmar eliminación",
                    key=f"chk_{confirm_key}"
                )

                if st.session_state[confirm_key]:
                    db.delete(c)
                    db.commit()
                    st.warning(f"Compra {c.id} eliminada.")
                    time.sleep(1)
                    st.session_state[del_key] = False
                    st.session_state[confirm_key] = False
                    st.rerun()


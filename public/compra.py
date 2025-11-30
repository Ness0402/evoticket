import streamlit as st
from database.connection import SessionLocal
from database.models import Evento, Compra, TicketType
from utils.qr_services import generar_qr
from utils.validaciones import es_mayor_edad
from utils.pdf_service import generar_pdf_ticket
import datetime

db = SessionLocal()
TIPOS_DOC = ["DUI", "Pasaporte", "Otro"]

def compra_tickets_ui():
    evento_id = st.session_state.get("evento_compra_id")
    evento = db.query(Evento).filter_by(id=evento_id).first()
    if not evento:
        st.error("Evento no encontrado.")
        return

    st.title(f"🎫 Compra de Tickets - {evento.nombre}")
    st.write(evento.descripcion)
    st.write(f"📅 Fecha: {evento.fecha}")
    st.write("---")

    nombres = st.text_input("Nombres")
    apellidos = st.text_input("Apellidos")
    tipo_doc = st.selectbox("Tipo de documento", TIPOS_DOC)
    documento = st.text_input("Número de documento")
    fecha_nac = st.date_input(
        "Fecha de nacimiento",
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today()
    )
    correo = st.text_input("Correo electrónico (para registro)")

    tickets_disponibles = db.query(TicketType).filter(
        TicketType.evento_id == evento.id,
        TicketType.cantidad_disponible > 0
    ).all()

    if not tickets_disponibles:
        st.warning("No hay tickets disponibles para este evento.")
        return

    opciones_ticket = {
        f"{t.categoria.nombre} - ${t.precio} - {t.cantidad_disponible} disponibles": t.id
        for t in tickets_disponibles
    }
    ticket_id = st.selectbox(
        "Selecciona el tipo de ticket",
        list(opciones_ticket.values()),
        format_func=lambda x: [k for k, v in opciones_ticket.items() if v == x][0]
    )

    ticket = db.query(TicketType).filter_by(id=ticket_id).first()

    cantidad = st.number_input(
        "Cantidad de tickets",
        min_value=1,
        max_value=ticket.cantidad_disponible
    )

    if st.button("Confirmar compra"):
        if not es_mayor_edad(fecha_nac):
            st.error("Debes ser mayor de edad para comprar tickets.")
            return

        if cantidad > ticket.cantidad_disponible:
            st.error(f"No hay suficientes tickets disponibles. Solo quedan {ticket.cantidad_disponible}.")
            return

        compra = Compra(
            evento_id=evento.id,
            nombres=nombres,
            apellidos=apellidos,
            documento=documento,
            tipo_documento=tipo_doc,
            fecha_nacimiento=fecha_nac,
            correo=correo,
            cantidad=cantidad
        )
        db.add(compra)

        ticket.cantidad_disponible -= cantidad

        db.commit()
        db.refresh(compra)

        qr_bytes = generar_qr(compra.qr_uuid)

        st.success("🎉 Compra realizada correctamente.")
        st.info("Puedes descargar tus tickets ahora. Si no los descargas, deberás presentar tu documento el día del evento.")

        pdf_bytes = generar_pdf_ticket(compra, evento, qr_bytes)

        st.download_button(
            label="📄 Descargar Tickets en PDF",
            data=pdf_bytes,
            file_name=f"ticket_{compra.id}.pdf",
            mime="application/pdf"
        )

        st.balloons()

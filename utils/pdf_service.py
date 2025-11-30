from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

TICKET_SIZE = (252, 576)

def generar_pdf_ticket(compra, evento, qr_bytes):

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=TICKET_SIZE)

    width, height = TICKET_SIZE

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 40, "🎫 Ticket de Entrada")

    c.setFont("Helvetica", 10)
    y = height - 80

    c.drawString(20, y, f"Evento: {evento.nombre}")
    y -= 14
    c.drawString(20, y, f"Fecha: {evento.fecha}")
    y -= 14
    c.drawString(20, y, f"Descripción: {evento.descripcion[:40]}...")
    y -= 25

    c.drawString(20, y, f"Nombre: {compra.nombres} {compra.apellidos}")
    y -= 14
    c.drawString(20, y, f"Documento: {compra.tipo_documento} - {compra.documento}")
    y -= 14
    c.drawString(20, y, f"Cantidad: {compra.cantidad}")
    y -= 30

    c.drawString(20, y, "Código QR:")
    y -= 10

    qr_img = ImageReader(BytesIO(qr_bytes))
    c.drawImage(qr_img, (width - 150) / 2, y - 150, width=150, height=150)

    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(
        width / 2,
        20,
        "Si no presentas este ticket deberás mostrar tu documento el día del evento."
    )

    c.save()
    pdf = buffer.getvalue()
    buffer.close()

    return pdf

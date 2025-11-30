import qrcode
from io import BytesIO

def generar_qr(code: str):
    img = qrcode.make(code)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

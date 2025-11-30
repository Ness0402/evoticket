from datetime import date

def es_mayor_edad(fecha):
    hoy = date.today()
    edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
    return edad >= 18

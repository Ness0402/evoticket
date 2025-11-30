from database.connection import engine
from database.models import Base

print("⏳ Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✔ Tablas creadas correctamente.")
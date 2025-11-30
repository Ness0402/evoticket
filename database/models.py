from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship

Base = declarative_base()

class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    fecha = Column(Date)

class TicketType(Base):
    __tablename__ = "ticket_types"
    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"))
    category_id = Column(Integer, ForeignKey("ticket_categories.id"))
    precio = Column(Float, nullable=False)
    cantidad_disponible = Column(Integer, default=0)
    categoria = relationship("TicketCategory")

class TicketCategory(Base):
    __tablename__ = "ticket_categories"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    role = Column(String)
    active = Column(Boolean, default=True)

    def verify_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode(), self.password.encode())
    
class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"))
    nombres = Column(String)
    apellidos = Column(String)
    documento = Column(String)
    tipo_documento = Column(String)
    fecha_nacimiento = Column(Date)
    correo = Column(String)
    cantidad = Column(Integer)
    qr_uuid = Column(String, default=lambda: str(uuid.uuid4()))
    fecha_compra = Column(DateTime, default=datetime.utcnow)

    evento = relationship("Evento")
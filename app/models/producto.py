from app.models.base import Base, TimestampMixin
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ProductoModel(Base, TimestampMixin):
    __tablename__ = "productos"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    activo = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database.connection import Base
import enum

class RolEnum(str, enum.Enum):
    admin = "admin"
    project_manager = "project_manager"
    developer = "developer"
    stakeholder = "stakeholder"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), default=RolEnum.developer, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    fecha_ultimo_login = Column(DateTime(timezone=True), onupdate=func.now())
    activo = Column(Integer, default=1)

    def __repr__(self):
        return f"<Usuario(id={self.id}, email={self.email}, nombre={self.nombre})>"



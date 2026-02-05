from app.database import Base
from sqlalchemy import Column, Integer, String,Date,  ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("usu_id", Integer, primary_key=True, index=True)
    nombre = Column("usu_nombre", String(100), nullable=False)
    email = Column("usu_email", String(100), nullable=False)
    rol = Column("usu_rol", String(10), nullable=False)
    ciudad = Column("usu_ciudad", String(50))
    pais = Column("usu_pais", String(50))
    descripcion = Column("usu_descripcion", Text)
    facebook = Column("usu_facebook", String(255))
    linkedin = Column("usu_linkedin", String(255))
    github = Column("usu_github", String(255))
    celular = Column("usu_celular", String(20))
    foto = Column("usu_fotoperfil", String(255), default="default.png")

    asesorias = relationship("Asesoria", back_populates="programador")

class Asesoria(Base):
    __tablename__ = "ASESORIAS"

    id = Column("ASES_ID", Integer, primary_key=True, index=True)
    fecha = Column("ASES_FECHA", Date)

    programador_id = Column(
        "ASES_ID_PROGRAMADOR_FK",
        Integer,
        ForeignKey("usuarios.usu_id"),
        nullable=False
    )

    programador = relationship("Usuario", back_populates="asesorias")

    horas = relationship(
        "HoraAsesoria",
        back_populates="asesoria",
        cascade="all, delete-orphan"
    )


class HoraAsesoria(Base):
    __tablename__ = "HORAS_ASESORIAS"

    id = Column("HORA_ID", Integer, primary_key=True, index=True)
    hora = Column("HORA_HORA", String(255))
    reservado = Column("HORA_RESERVADO", String(1))

    asesoria_id = Column(
        "HORA_ID_ASESORIA_FK",
        Integer,
        ForeignKey("ASESORIAS.ASES_ID"),  
        nullable=False
    )

    asesoria = relationship(
        "Asesoria",
        back_populates="horas"
    )


class ReservaAsesoria(Base):
    __tablename__ = "RESERVA_ASESORIA"

    id = Column("RESA_ID", Integer, primary_key=True, index=True)
    motivo = Column("RESA_MOTIVO", String(255))
    estado = Column("RESA_ESTADO", String(20), default="PENDIENTE")

    asesoria_id = Column("RESA_ID_ASESORIA", Integer, nullable=False)
    hora_asesoria_id = Column("RESA_ID_HORA_ASESORIA", Integer, nullable=False)
    solicitante_id = Column("RESA_ID_SOLICITANTE", Integer, nullable=False)
    programador_id = Column("RESA_ID_PROGRAMADOR", Integer, nullable=False)

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from datetime import date


class UsuarioBase(BaseModel):
    nombre: str
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    descripcion: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    celular: Optional[str] = None
    github: Optional[str] = None
    email: str
    rol: str
    foto: str = "default.png"

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int
    model_config = {"from_attributes": True}

class AsesoriaBase(BaseModel):
    fecha: date
    programador_id: int

class AsesoriaCreate(AsesoriaBase):
    pass

class AsesoriaResponse(AsesoriaBase):
    id: int
    model_config = {"from_attributes": True}


class HoraAsesoriaBase(BaseModel):
    hora: str
    asesoria_id: int

class HoraAsesoriaCreate(HoraAsesoriaBase):
    pass

class HoraAsesoriaResponse(HoraAsesoriaBase):
    id: int
    reservado: str
    model_config = {"from_attributes": True}


class ReservaAsesoriaBase(BaseModel):
    motivo: str | None = None
    asesoria_id: int
    hora_asesoria_id: int
    solicitante_id: int
    programador_id: int

class ReservaAsesoriaCreate(ReservaAsesoriaBase):
    pass

class ReservaAsesoriaResponse(ReservaAsesoriaBase):
    id: int
    estado: str
    model_config = {"from_attributes": True}


class UsuarioSimple(BaseModel):
    id: int
    nombre: str
    email: str

    model_config = {"from_attributes": True}


class ReservaDetalleResponse(BaseModel):
    id: int
    motivo: str | None
    estado: str
    fecha: date
    hora: str
    programador: UsuarioSimple
    solicitante: UsuarioSimple

class DisponibilidadCreate(BaseModel):
    idProgramador: int
    fecha: date
    horaInicio: str
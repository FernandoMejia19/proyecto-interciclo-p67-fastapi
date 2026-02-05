from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, get_db
from app import models, schemas
from app.router import reservas

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], # Tu puerto de Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Crear tablas si no existen
#models.Base.metadata.create_all(bind=engine)

# =========================
# USUARIOS
# =========================
@app.post("/usuarios", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    nuevo = models.Usuario(**usuario.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.get("/usuarios", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


# =========================
# ASESORIAS
# =========================
@app.post("/asesorias", response_model=schemas.AsesoriaResponse)
def crear_asesoria(data: schemas.AsesoriaCreate, db: Session = Depends(get_db)):
    nueva = models.Asesoria(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@app.get("/asesorias/programador/{id_programador}", response_model=list[schemas.AsesoriaResponse])
def listar_asesorias_programador(id_programador: int, db: Session = Depends(get_db)):
    return db.query(models.Asesoria)\
        .filter(models.Asesoria.programador_id == id_programador)\
        .all()


# =========================
# HORAS ASESORIA
# =========================
@app.post("/horas-asesoria", response_model=schemas.HoraAsesoriaResponse)
def crear_hora(data: schemas.HoraAsesoriaCreate, db: Session = Depends(get_db)):
    hora = models.HoraAsesoria(
        hora=data.hora,
        asesoria_id=data.asesoria_id,
        reservado="N"
    )
    db.add(hora)
    db.commit()
    db.refresh(hora)
    return hora


@app.get("/horas-asesoria/{asesoria_id}", response_model=list[schemas.HoraAsesoriaResponse])
def listar_horas(asesoria_id: int, db: Session = Depends(get_db)):
    return db.query(models.HoraAsesoria)\
        .filter(
            models.HoraAsesoria.asesoria_id == asesoria_id,
            models.HoraAsesoria.reservado == "N"
        ).all()


# =========================
# RESERVAS
# =========================
app.include_router(reservas.router)

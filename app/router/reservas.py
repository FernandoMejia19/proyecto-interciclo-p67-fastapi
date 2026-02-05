from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.post("/disponibilidad")
def crear_disponibilidad(
    data: schemas.DisponibilidadCreate,
    db: Session = Depends(get_db)
):
    asesoria = models.Asesoria(
        programador_id=data.idProgramador,
        fecha=data.fecha
    )
    db.add(asesoria)
    db.commit()
    db.refresh(asesoria)

    hora = models.HoraAsesoria(
        asesoria_id=asesoria.id,
        hora=data.horaInicio,
        reservado="N"
    )
    db.add(hora)
    db.commit()

    return {"mensaje": "Disponibilidad creada"}

@router.post("/", response_model=schemas.ReservaAsesoriaResponse)
def crear_reserva(
    data: schemas.ReservaAsesoriaCreate,
    db: Session = Depends(get_db)
):
    # 1️ Buscar la hora
    hora = db.query(models.HoraAsesoria).filter(
        models.HoraAsesoria.id == data.hora_asesoria_id
    ).first()

    if not hora:
        raise HTTPException(status_code=404, detail="Hora no encontrada")

    # 2️ Verificar si ya está reservada
    if hora.reservado == "S":
        raise HTTPException(
            status_code=400,
            detail="Esta hora ya fue reservada"
        )

    # 3️ Crear la reserva
    reserva = models.ReservaAsesoria(**data.model_dump())
    db.add(reserva)

    # 4️ Marcar la hora como reservada
    hora.reservado = "S"

    # 5️ Guardar todo
    db.commit()
    db.refresh(reserva)

    return reserva



@router.put("/reservas/{reserva_id}/estado")
def cambiar_estado(
    reserva_id: int,
    estado: str,
    db: Session = Depends(get_db)
):
    reserva = db.query(models.ReservaAsesoria)\
        .filter(models.ReservaAsesoria.id == reserva_id)\
        .first()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    reserva.estado = estado
    db.commit()

    return {"mensaje": f"Reserva actualizada a {estado}"}

@router.get(
    "/solicitante/{solicitante_id}",
    response_model=list[schemas.ReservaAsesoriaResponse]
)
def reservas_por_solicitante(
    solicitante_id: int,
    db: Session = Depends(get_db)
):
    return db.query(models.ReservaAsesoria)\
        .filter(models.ReservaAsesoria.solicitante_id == solicitante_id)\
        .all()

@router.get(
    "/detalle/{reserva_id}",
    response_model=schemas.ReservaDetalleResponse
)
def obtener_reserva_detalle(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.query(models.ReservaAsesoria).filter(
        models.ReservaAsesoria.id == reserva_id
    ).first()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    asesoria = db.query(models.Asesoria).filter(
        models.Asesoria.id == reserva.asesoria_id
    ).first()

    hora = db.query(models.HoraAsesoria).filter(
        models.HoraAsesoria.id == reserva.hora_asesoria_id
    ).first()

    programador = db.query(models.Usuario).filter(
        models.Usuario.id == reserva.programador_id
    ).first()

    solicitante = db.query(models.Usuario).filter(
        models.Usuario.id == reserva.solicitante_id
    ).first()

    return {
        "id": reserva.id,
        "motivo": reserva.motivo,
        "estado": reserva.estado,
        "fecha": asesoria.fecha,
        "hora": hora.hora,
        "programador": programador,
        "solicitante": solicitante
    }

@router.put("/cancelar/{reserva_id}")
def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.query(models.ReservaAsesoria).filter(
        models.ReservaAsesoria.id == reserva_id
    ).first()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    # 1 cambiar estado
    reserva.estado = "CANCELADA"

    # 2 liberar hora
    hora = db.query(models.HoraAsesoria).filter(
        models.HoraAsesoria.id == reserva.hora_asesoria_id
    ).first()

    if hora:
        hora.reservado = "N"

    db.commit()

    return {
        "message": "Reserva cancelada correctamente"
    }


@router.get("/usuario/{usuario_id}", response_model=list[schemas.ReservaAsesoriaResponse])
def reservas_por_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    return db.query(models.ReservaAsesoria).filter(
        models.ReservaAsesoria.solicitante_id == usuario_id
    ).all()


@router.get("/programador/{programador_id}", response_model=list[schemas.ReservaAsesoriaResponse])
def reservas_por_programador(
    programador_id: int,
    db: Session = Depends(get_db)
):
    return db.query(models.ReservaAsesoria).filter(
        models.ReservaAsesoria.programador_id == programador_id
    ).all()

from fastapi import HTTPException

@router.put("/{reserva_id}/estado")
def cambiar_estado_reserva(
    reserva_id: int,
    estado: str,
    db: Session = Depends(get_db)
):
    reserva = db.query(models.ReservaAsesoria).filter(
        models.ReservaAsesoria.id == reserva_id
    ).first()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    estados_validos = ["PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"]

    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail="Estado inválido")

    reserva.estado = estado
    db.commit()
    db.refresh(reserva)

    return reserva



@router.put("/{reserva_id}/cancelar")
def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.query(models.ReservaAsesoria).filter(
        models.ReservaAsesoria.id == reserva_id
    ).first()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    # Cambiar estado de la reserva
    reserva.estado = "CANCELADA"

    # Liberar la hora
    hora = db.query(models.HoraAsesoria).filter(
        models.HoraAsesoria.id == reserva.hora_asesoria_id
    ).first()

    if hora:
        hora.reservado = "N"

    db.commit()

    return {
        "mensaje": "Reserva cancelada correctamente"
    }

@router.get("/cliente/{cliente_id}")
def reservas_por_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    reservas = db.query(models.ReservaAsesoria).filter(
        models.ReservaAsesoria.solicitante_id == cliente_id
    ).all()

    return reservas




from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

app = FastAPI(title="API de tareas")


# =========================
# SCHEMAS
# =========================

class TareaCreate(BaseModel):
    id: int
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str = Field(min_length=1, max_length=100)
    completada: bool = False
    prioridad: Literal["alta", "media", "baja"] = "alta"


class TareaUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, min_length=1, max_length=100)
    completada: bool | None = None
    prioridad: Literal["alta", "media", "baja"] | None = None


class TareaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    completada: bool
    prioridad: Literal["alta", "media", "baja"]

    model_config = ConfigDict(from_attributes=True)

tareas_bd = []


# =========================
# OBTENER TODAS LAS TAREAS
# =========================

@app.get("/tareas", response_model=list[TareaResponse])
def obtener_tareas():
    return tareas_bd


# =========================
# CREAR UNA TAREA
# =========================

@app.post("/tareas", status_code=201, response_model=TareaResponse)
def crear_tarea(tarea: TareaCreate):
    for t in tareas_bd:
        if t["id"] == tarea.id:
            raise HTTPException(
                status_code=400,
                detail="El ID de la tarea ya existe"
            )

    nueva_tarea = tarea.model_dump()
    tareas_bd.append(nueva_tarea)

    return nueva_tarea


# =========================
# ACTUALIZAR UNA TAREA COMPLETA
# =========================

@app.put("/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(tarea_id: int, tarea_actualizada: TareaCreate):
    for i, tarea in enumerate(tareas_bd):
        if tarea["id"] == tarea_id:
            datos_nuevos = tarea_actualizada.model_dump()
            datos_nuevos["id"] = tarea_id
            tareas_bd[i] = datos_nuevos

            return datos_nuevos

    raise HTTPException(
        status_code=404,
        detail="La tarea no fue encontrada"
    )


# =========================
# ACTUALIZAR UNA TAREA PARCIALMENTE
# =========================

@app.patch("/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_parcialmente(tarea_id: int, cambios: TareaUpdate):
    for i, tarea in enumerate(tareas_bd):
        if tarea["id"] == tarea_id:
            datos_nuevos = cambios.model_dump(exclude_unset=True)

            if not datos_nuevos:
                raise HTTPException(
                    status_code=422,
                    detail="Debes enviar al menos un campo para actualizar"
                )

            if any(valor is None for valor in datos_nuevos.values()):
                raise HTTPException(
                    status_code=422,
                    detail="Los campos enviados no pueden ser null"
                )

            tareas_bd[i].update(datos_nuevos)
            return tareas_bd[i]

    raise HTTPException(
        status_code=404,
        detail="La tarea no fue encontrada"
    )


# =========================
# ELIMINAR UNA TAREA
# =========================

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    for i, tarea in enumerate(tareas_bd):
        if tarea["id"] == tarea_id:
            tareas_bd.pop(i)

            return {"mensaje": "Tarea eliminada con éxito"}

    raise HTTPException(
        status_code=404,
        detail="La tarea no fue encontrada"
    )
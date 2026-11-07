import sqlite3

from fastapi import Depends, FastAPI, HTTPException

import schemas
from database import crear_tablas, get_connection

# Crea la tabla si no existe
crear_tablas()

app = FastAPI()


# Dependencia: abre una conexión por petición y la cierra al terminar
def get_db():
    db = get_connection()
    try:
        yield db
    finally:
        db.close()


@app.post("/tareas", response_model=schemas.TareaLeer, status_code=201)
def crear_tarea(datos: schemas.TareaCrear, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute(
        "INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)",
        (datos.titulo, datos.descripcion),
    )
    db.commit()
    fila = db.execute("SELECT * FROM tareas WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return dict(fila)


@app.get("/tareas/{tarea_id}", response_model=schemas.TareaLeer)
def obtener_tarea(tarea_id: int, db: sqlite3.Connection = Depends(get_db)):
    fila = db.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
    if not fila:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return dict(fila)

@app.delete("/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")


@app.get("/tareas", response_model=list[schemas.TareaLeer])
def listar_tareas(completada: bool | None = None, db: sqlite3.Connection = Depends(get_db)):
    if completada is None:
        filas = db.execute("SELECT * FROM tareas").fetchall()
    else:
        filas = db.execute(
            "SELECT * FROM tareas WHERE completada = ?", (int(completada),)
        ).fetchall()
    return [dict(f) for f in filas]
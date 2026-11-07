from pydantic import BaseModel


# Lo que el cliente envía al crear una tarea
class TareaCrear(BaseModel):
    titulo: str
    descripcion: str | None = None


# Lo que la API devuelve
class TareaLeer(BaseModel):
    id: int
    titulo: str
    completada: bool
    descripcion: str | None = None

import sqlite3

DB_FILE = "tareas.db"


def get_connection():
    # check_same_thread=False: FastAPI atiende las peticiones en distintos hilos
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    # row_factory: permite acceder a las columnas por nombre y convertir cada fila a dict
    conn.row_factory = sqlite3.Row
    return conn


def crear_tablas():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            completada INTEGER NOT NULL DEFAULT 0,
            descripcion TEXT
        )
        """
    )
    columnas = conn.execute("PRAGMA table_info(tareas)").fetchall()
    if not any(columna["name"] == "descripcion" for columna in columnas):
        conn.execute("ALTER TABLE tareas ADD COLUMN descripcion TEXT")
    conn.commit()
    conn.close()

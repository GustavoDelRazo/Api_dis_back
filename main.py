import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Crea la base de datos
conn = sqlite3.connect("sql/dispositivos.db")

app = fastapi.FastAPI()

origins = [
    "http://localhost:8080",
    "https://shm-frontend-c3f2dc0fa89c.herokuapp.com",
    "https://api-contactos-frontend-a3d16e92dede.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Dispositivo(BaseModel):
    id : int
    dispositivo : str
    valor: int

class DispositivoPUT(BaseModel):
    valor: int


@app.get("/")
async def root():
    return "Conexion exitosa"

@app.get("/dispositivos")
async def get_all():
    """Obtiene todos los contactos."""
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos;')
    response = []
    for row in c:
        dispositivo = {"id":row[0],"dispositivo":row[1], "valor":row[2]}
        response.append(dispositivo)
    return response

@app.get("/dispositivos/{id}")
async def get_dispositivo(id: int):
    """Obtiene un contacto por su email."""
    # Consulta el contacto por su email
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos WHERE id = ?', (id,))
    dispositivo = None
    for row in c:
         dispositivo = {"id":row[0],"dispositivo":row[1], "valor":row[2]}
    return dispositivo

@app.put("/dispositivos/{id}")
async def get_dispositivo(id: int, dispositivo: DispositivoPUT):
    """Obtiene un contacto por su email."""
    # Consulta el contacto por su email
    c = conn.cursor()
    c.execute('UPDATE dispositivos SET valor = ? WHERE id = ?;',
              (dispositivo.valor,id))
    conn.commit()
    return dispositivo
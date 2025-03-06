from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import routes, database

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen (para desarrollo local)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(routes.router)

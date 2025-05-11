from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import movimientos

app = FastAPI()

# Habilita CORS para conectar con Svelte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movimientos.router, 
                   prefix="/movimientos", 
                   tags=["Movimientos"])

@app.get("/")
def read_root():
    return {"message": "API funcionando"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import movimientos

app = FastAPI()

# Titicash 2
# Habilita CORS para conectar con Svelte
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://titicash.vercel.app"
    ],
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
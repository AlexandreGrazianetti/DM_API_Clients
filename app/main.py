from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.routes import client_router
from app import models

# Création des tables dans la base de données
models.Base.metadata.create_all(bind=engine)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Client API",
    description="API pour la gestion des clients",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(client_router)

@app.get("/")
def read_root():
    """Endpoint racine de l'API."""
    return {"message": "Bienvenue sur l'API de gestion des clients"}
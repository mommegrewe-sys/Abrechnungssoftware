from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import partners
from app.database import Base, engine

app = FastAPI(title="Abrechnungssoftware API")

# Tabellen erstellen
Base.metadata.create_all(bind=engine)

# ✅ CORS konfigurieren
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router einbinden
app.include_router(partners.router, prefix="/partners", tags=["Partners"])

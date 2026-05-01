from fastapi import FastAPI
from db import get_latest_partidos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {"mensaje": "API funcionando 🚀"}


@app.get("/partidos")
def get_partidos():
    return get_latest_partidos()

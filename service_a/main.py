import databases
import os
import time
from fastapi import FastAPI
import logging
import httpx

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@postgres_db:5432/mydatabase"

database = databases.Database(DATABASE_URL)
app = FastAPI()

ADMIN_API_URL = "http://service_b:8001"

@app.on_event("startup")
async def startup():
    logging.info("Service A - Connexion à la base de données...")
    await database.connect()
    logging.info("Service A - Connecté.")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logging.info("Service A - Déconnecté.")

from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

@app.post("/add_user")
async def add_user(user: UserCreate):
    query = "INSERT INTO users (name) VALUES (:name)"
    await database.execute(query, {"name": user.name})
    return {"message": "User added"}


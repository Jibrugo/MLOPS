from fastapi import FastAPI
import databases
import logging

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@postgres_db:5432/mydatabase"

database = databases.Database(DATABASE_URL)
app = FastAPI()

@app.on_event("startup")
async def startup():
    logging.info("Service B - Connexion à la base de données...")
    await database.connect()
    logging.info("Service B - Connecté.")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logging.info("Service B - Déconnecté.")

@app.post("/insert_user")
async def insert_user(name: str):
    query = "INSERT INTO users (name) VALUES (:name)"
    await database.execute(query, {"name": name})
    return {"message": "User added"}

@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    users = await database.fetch_all(query)
    return {"users": users}

@app.put("/update_user/{user_id}")
async def update_user(user_id: int, name: str):
    query = "UPDATE users SET name = :name WHERE id = :id"
    await database.execute(query, {"id": user_id, "name": name})
    return {"message": "User updated"}

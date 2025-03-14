from fastapi import FastAPI
import databases
import os
import logging
import httpx
import time 

# Le fichier Unix Socket pour PostgreSQL
SOCKET_PATH = "/tmp/service_a_socket"

# Connexion à PostgreSQL via Unix Socket
DATABASE_URL = f"postgresql+asyncpg://myuser:mypassword@postgres_db:5432/mydatabase"

database = databases.Database(DATABASE_URL)
app = FastAPI()

# Fonction pour vérifier la disponibilité du socket
def wait_for_socket():
    while not os.path.exists(SOCKET_PATH):
        logging.info(f"Socket {SOCKET_PATH} non trouvé, en attente...")
        time.sleep(1)  # Attente de 1 seconde avant de réessayer

@app.on_event("startup")
async def startup():
    logging.info("Service B - Tentative de connexion à la base de données...")
    wait_for_socket()  # Attendre que le socket soit créé
    await database.connect()
    logging.info("Service B - Connexion à la base de données réussie.")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logging.info("Service B - Déconnexion de la base de données.")

@app.post("/add_user")
async def add_user(name: str):
    query = "INSERT INTO users (name) VALUES (:name)"
    await database.execute(query, {"name": name})
    return {"message": "User added"}

@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    users = await database.fetch_all(query)
    return {"users": users}

# Endpoint pour récupérer les utilisateurs depuis service_a via Unix Domain Socket
@app.get("/users_from_service_a")
async def get_users_from_service_a():
    # Utilisation de httpx pour faire une requête HTTP via le socket Unix
    SERVICE_A_URL = f"http+unix://{SOCKET_PATH}/users"  # L'URL vers service_a
    async with httpx.AsyncClient() as client:
        response = await client.get(SERVICE_A_URL)
    return response.json()

# Lancer le serveur FastAPI sur Unix Domain Socket
if __name__ == "__main__":
    logging.info(f"Service B - Démarrage du serveur sur {SOCKET_PATH}")
    import uvicorn
    uvicorn.run(app, unix_socket=SOCKET_PATH)

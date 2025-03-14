import databases
import os
import time
from fastapi import FastAPI
import logging

# Le fichier Unix Socket
SOCKET_PATH = "/tmp/service_a_socket"

# Remplacer DATABASE_URL pour se connecter via socket
DATABASE_URL = f"postgresql+asyncpg://myuser:mypassword@postgres_db:5432/mydatabase"

database = databases.Database(DATABASE_URL)
app = FastAPI()

# Fonction pour vérifier si le socket est disponible
def wait_for_socket():
    while not os.path.exists(SOCKET_PATH):
        logging.info(f"Socket {SOCKET_PATH} non trouvé, en attente...")
        time.sleep(1)  # Attente de 1 seconde avant de réessayer

@app.on_event("startup")
async def startup():
    logging.info("Service A - Tentative de connexion à la base de données...")
    wait_for_socket()  # Attendre que le socket soit créé
    await database.connect()
    logging.info("Service A - Connexion à la base de données réussie.")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logging.info("Service A - Déconnexion de la base de données.")

@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    users = await database.fetch_all(query)
    return {"users": users}

# Lancer le serveur FastAPI sur Unix Domain Socket
if __name__ == "__main__":
    import uvicorn
    logging.info(f"Service A - Démarrage du serveur sur {SOCKET_PATH}")
    uvicorn.run(app, unix_socket=SOCKET_PATH)

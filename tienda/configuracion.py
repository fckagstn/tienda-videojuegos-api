from dotenv import load_dotenv
import os

load_dotenv()

db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
llave = os.getenv("LLAVE")
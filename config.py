from dotenv import load_dotenv
import os


load_dotenv()
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_port = int(os.getenv('DB_PORT'))
db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_DATABASE')

ERR      = -1
SUCCESS  = 0
DUP      = -2 # duplicate record
import databases
import sqlalchemy
from decouple import config

DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:{config('DB_PORT')}/{config('DB_NAME')}"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

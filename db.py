import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():         # Abre una conexión temporal para hacer una operación sobre la base de datos
    return psycopg2.connect(        # Abre una conexión real a PostgreSQL con los datos de las siguientes líneas (usuario, puerto...)
        host=os.getenv("POSTGRES_HOST", "db"),   
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "devdb"),
        user=os.getenv("POSTGRES_USER", "devuser"),
        password=os.getenv("POSTGRES_PASSWORD", "devpass"),
        cursor_factory=RealDictCursor)
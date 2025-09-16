import os
import psycopg2
from psycopg2.extras import RealDictCursor

_conn = None

def get_conn():
    global _conn
    if _conn is None or _conn.closed:
        _conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=5432
        )
    return _conn

def get_cursor():
    conn = get_conn()
    return conn, conn.cursor(cursor_factory=RealDictCursor)
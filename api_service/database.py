import psycopg2 as pg
import os

HOST = os.getenv("NET_NAME", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PWD = os.getenv("DB_PWD", "postgres")

ENGINE = lambda: pg.connect(
    f"dbname='{DB_NAME}' user='{DB_USER}' host='{HOST}' port='{DB_PORT}' password='{DB_PWD}'"
)

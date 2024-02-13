from utils.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, logger

import psycopg2
import os
from datetime import datetime
import subprocess


def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        conn.autocommit = True
        logger.info("Connection established.")
    except:
        logger.info("Can`t establish connection to database.")

    return conn


def connect_to_database(conn):
    cursor = conn.cursor()
    sql_create_db = """
        CREATE TABLE IF NOT EXISTS car_cards (
        url TEXT,
        title TEXT,
        price_usd INTEGER,
        odometer INTEGER,
        username TEXT,
        phone_number BIGINT,
        image_url TEXT,
        images_count SMALLINT,
        car_number TEXT,
        car_vin TEXT,
        datetime_found TIMESTAMP
    );"""
    cursor.execute(sql_create_db)
    logger.info("Sucessfully connected to database")

    cursor.close()


def get_urls_from_database(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM car_cards;")
    all_urls = [item[0] for item in cursor.fetchall()]

    cursor.close()

    return all_urls


def insert_row(conn, rows):
    cursor = conn.cursor()
    sql_insert = """
        INSERT INTO car_cards
        VALUES {}""".format(*rows)
    cursor.execute(sql_insert)

    cursor.close()


def create_database_dump():
    current_time = datetime.now().strftime("%d-%m-%Y")
    filename = f"{DB_NAME}_{current_time}.sql"
    dest_file = os.path.join(os.getcwd(), "dumps", filename)

    logger.info("Sucessfully created database dump.")
    subprocess.Popen('pg_dump --dbname=postgresql://{}:{}@{}:{}/{} -f {}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, dest_file))

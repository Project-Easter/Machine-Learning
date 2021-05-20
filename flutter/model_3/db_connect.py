import psycopg2
from config import get_credentials

def connect():

    database, username, password, hostname, port = get_credentials()

    connection = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname,
        port = port
    )

    return connection


def fetch(query):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print("Query executed.....")
    cursor.close()
    conn.close()
    return records, columns

def update(query):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    print("Database updated.....")
    conn.close()



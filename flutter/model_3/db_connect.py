import psycopg2
from config import get_credentials

database, username, password, hostname, port = get_credentials()

connection = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname,
    port = port
)

cursor = connection.cursor()


def fetch(query):
    cursor.execute(query)
    records = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print("Query executed.....")
    return records, columns

def update(query):
    cursor.execute(query)
    connection.commit()
    print("Database updated.....")

def close_connection(cursor):
    cursor.close()
    connection.close()

close_connection(cursor)

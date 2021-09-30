"""
This module contains methods to connect to the datbase and perform fetch and update operations on it. The database connection
is established using psycopg2.
"""

import psycopg2
from flutter.model_3.config import get_credentials

def connect():

    """
    Function to connect to the database.

    Returns:
    connection variable
    """

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
    """
    Function to fetch data from the database.
    """
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
    """
    Function to insert rows into the database.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    print("Database updated.....")
    conn.close()



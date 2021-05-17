import psycopg2
from config import get_credentials
# import pandas as pd

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
    print("Query executed.....")
    return records

def update(query):
    cursor.execute(query)
    connection.commit()
    print("Database updated.....")

# x = pd.DataFrame(fetch("SELECT * FROM \"Book\";"))
# x.to_csv("data.csv")
x = fetch("SELECT * FROM \"Book\" LIMIT 10;")
print(x)
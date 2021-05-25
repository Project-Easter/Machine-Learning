# Files containing database configs
from urllib.parse import urlparse
import os 
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_credentials():
    db_url = urlparse(DATABASE_URL)
    DB_USERNAME = db_url.username
    DB_PASSWORD = db_url.password 
    DB_DATABASE = db_url.path[1:]
    DB_HOSTNAME = db_url.hostname
    DB_PORT = db_url.port

    return DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_PORT  
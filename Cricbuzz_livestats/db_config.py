import pymysql

HOST = "localhost"
USER = "root"           # your MySQL username
PASSWORD = "root"       # your MySQL password
DATABASE = "cricbuzz_db"

def get_connection():
    return pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )


from database.db_connect import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("INSERT INTO trainer (name, email, password) VALUES (?, ?, ?)", 
               ("Vinay", "vinay@gmail.com", "12345"))

conn.commit()
conn.close()

print("Trainer Inserted!")



def create_trainer_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainer (
            trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_client_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            goal TEXT
        )
    ''')
    conn.commit()
    conn.close()
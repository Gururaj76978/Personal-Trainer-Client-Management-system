import sqlite3

def get_connection():
    conn = sqlite3.connect('trainer_db.db')  # Database File
    return conn


def add_client(name, age, gender, weight, height, goal, trainer_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO client (name, age, gender, weight, height, goal, trainer_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, gender, weight, height, goal, trainer_name))
    conn.commit()
    conn.close()

def view_clients(trainer_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client WHERE trainer_name=?", (trainer_name,))
    data = cursor.fetchall()
    conn.close()
    return data

def update_client(client_id, name, age, gender, weight, height, goal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE client SET name=?, age=?, gender=?, weight=?, height=?, goal=? WHERE client_id=?", 
                   (name, age, gender, weight, height, goal, client_id))
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM client WHERE client_id=?", (client_id,))
    conn.commit()
    conn.close()


def get_client_by_id(client_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM client WHERE client_id = ?", (client_id,))
    data = cursor.fetchone()
    conn.close()
    return data
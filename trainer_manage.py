from database.db_connect import get_connection as connect
def add_trainer(name, username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO trainer (name, username, password) VALUES (?, ?, ?)',
                (name, username, password))
    conn.commit()
    conn.close()

# View Trainers
def view_trainers():
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM trainer')
    data = cur.fetchall()
    conn.close()
    return data

# Update Trainer
def update_trainer(trainer_id, name, username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        UPDATE trainer
        SET name=?, username=?, password=? 
        WHERE id=?
        ''', (name, username, password, trainer_id))
    conn.commit()
    conn.close()

# Delete Trainer
def delete_trainer(trainer_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM trainer WHERE id=?', (trainer_id,))
    conn.commit()
    conn.close()

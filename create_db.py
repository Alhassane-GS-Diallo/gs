import sqlite3 as sq

conn = sq.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
   CREATE TABLE IF NOT EXISTS users (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT UNIQUE,
       user_id INTEGER,
       password TEXT,
       first_name TEXT,
       last_name TEXT
   )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        payment_method TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')
conn.commit()
recup = "SELECT * FROM users ;"
cursor.execute(recup)
data = cursor.fetchall()
print(data)
conn.close()
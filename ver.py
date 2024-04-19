import sqlite3
DATABASE = 'database.db'
def update_database_structure():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('ALTER TABLE users ADD COLUMN last_payment_date TIMESTAMP DEFAULT NULL')
        conn.commit()
        print("Mise à jour reussi")
    except sqlite3.Error as e :
        print(f"Erreur {e}")
    finally:
        conn.close()
if __name__ == '__main__':
    update_database_structure()
import time
from app import db_connection, clear

def main(username, password):
    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        cursor.fetchall()
        db.commit()
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            print("Akses berhasil ditambahkan !")
            time.sleep(2)
            clear()
        else:
            print("Username atau password sudah digunakan, silahkan buat yang lain")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        db.close()
        cursor.close()
                
username = input("Silahkan buat username: ")
password = input("Silahkan buat password: ")
main(username, password)
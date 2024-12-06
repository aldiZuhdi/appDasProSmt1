import time
import mysql.connector
# from app import db_connection, clear

def db_connection():
    try: # Mencoba membuat koneksi kedalam database
        # Membuat koneksi dengan format:
        return mysql.connector.connect(  
            host = 'localhost', 
            user = 'root', 
            password = '', 
            database = 'db_minimarket' 
        )
    # Sintaks yang berjalan jika terjadi error pada kode try  
    except mysql.connector.Error as e: # Menampilkan bagian yang error dari try koneksi ke MySQL
        print(f"Error: {e}") 
        time.sleep(5) # Membuat delay selama 5 detik sebelum mengeskekusi sintaks selanjutnya
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

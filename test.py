from app import db_connection, clear,main
import time


users = [
    {
        'username' : 'admin',
        'username' : 'user',
        'username' : 'budi',
        'password' : 'admin',
        'password' : 'user',
        'password' : 'budi'
    }
]

def login(username, password): 
    try:
        for user in users:
            if user['username'] == username and user['password'] == password:
                clear()
                print("\n\033[32m\033[1m!--Login Berhasil--!\033[0m\033[37m\n") # Alert keterangan untuk user
                time.sleep(2)
                clear()
                main()
            else:
                clear()
                print("\n\033[31m\033[1m!--Login Gagal--!\nusername atau password salah\033[0m\033[37m\n") # Alert keterangan untuk user
                time.sleep(1) # Membuat delay waktu selama 1 detik kepada terminal sebelum mengeksekusi sintaks selanjutnya
                clear() # Function clear
    except ValueError as e:
        print(f"Error: {e}")
        time.sleep(2)
        clear()
        main()

username = input("Masukkan username: ")
password = input("Masukkan password: ")
login(username, password)
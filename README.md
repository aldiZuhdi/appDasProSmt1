Font Color:
30m = Black color
31m = Red color
32m = Green color
33m = Yellow color
34m = Blue color
35m = Purple color
36m = Cyan color
37m = White color

Background Color:
40m = Black background
41m = Red background
42m = Green background
43m = Yellow background
44m = Blue background
45m = Purple background
46m = Cyan background
47m = White background

Fonts Style:
0m = Normal fonts
1m = Bold fonts
3m = Italic fonts
4m = Underline fonts
9m = Strikethrough fonts

HOW TO CONFIG GITHUB:

1. open TERMINAL
2. git init
3. git branch -M main
4. git remote add origin https://linkRepositoryGithub
5. git config --global user.name "username github"
6. git config --global user.email "email github"

HOW TO PUSH AND PULL GITHUB:

1. buka folder yang sudah dikonfigurasi dengan git
2. klik kanan di kanvas putih
3. buka git bash atau terminal windows powershell
4. ketikkan sintaks dibawah

PUSH:

1. git init
2. git add . (jika hanya ingin push 1 file maka setelah add ditambah dengan nama file)
3. git commit -m "diganti dengan pesan yang ingin kamu sampaikan"
4. git push origin main

PULL:

1. git init
2. git pull origin main

def login(username, password):
try: # Mencoba untuk fetch data sesuai dengan yang diinput oleh user (jika data True)
db = db_connection() # Mendeklarasikan variable untuk function db_connection
cursor = db.cursor() # Membuat cursor kedalam SQL
cursor.execute("SELECT \* FROM users WHERE username = %s AND password = %s", (username, password)) # Cursor mengeksekusi query untuk memilih column yang sesuai dengan yang diinput user berdasarkan parameter function
get_user = cursor.fetchone() # Fetch 1 data dari kolom table
if get_user: # Jika data berhasil di fetch
clear() # Function clear
print("\n\033[32m\033[1m!--Login Berhasil--!\033[0m\033[37m\n") # Alert keterangan untuk user
time.sleep(1) # Membuat delay waktu selama 1 detik kepada terminal sebelum mengeksekusi sintaks selanjutnya
clear() # Function clear
main() # Function main
else: # Jika data yang di fetch tidak cocok
clear() # Function clear
print("\n\033[31m\033[1m!--Login Gagal--!\nusername atau password salah\033[0m\033[37m\n") # Alert keterangan untuk user
time.sleep(1) # Membuat delay waktu selama 1 detik kepada terminal sebelum mengeksekusi sintaks selanjutnya
clear() # Function clear
except ValueError as e: # Menampilkan value yang error dari kolom try login
print(f"Error: {e}")  
 finally: # setelah selesai, tutup koneksi dan kursor untuk menghemat RAM
cursor.close() # Menutup cursor
db.close() # Menutup koneksi untuk menghemat memori

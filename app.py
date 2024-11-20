# Aplikasi pengadaan barang dengan operasi SQL CRUD (Create, Read, Update, Delete)
# Install Xampp
# Nyalakan Apache dan Mysql
# search di browser localhost
# pilih phpMyAdmin
# masuk ke menu sql
# Paste sintaks dibawah ini (digunakan hanya untuk petama kali saja untuk mengkonfigurasi database):

# CREATE DATABASE db_minimarket;
# USE db_minimarket;

# CREATE TABLE tb_product (
#     id INT(11) AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     category VARCHAR(255) NOT NULL,
#     weight INT(11) NOT NULL,
#     quantity INT(11) NOT NULL,
#     supplier VARCHAR(255) NOT NULL
# );

# CREATE TABLE users (
#     id INT(11) AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(16) NOT NULL,
#     password VARCHAR(16) NOT NULL,
#     position VARCHAR(25) NOT NULL
# );

# INSERT INTO `users` (`id`, `username`, `password`, `position`) VALUES (NULL, 'admin', 'admin', 'admin');

# INSERT INTO tb_product (id)
# VALUES (
#     CONCAT(
#         CHAR(FLOOR(65 + (RAND() * 26))),  -- Huruf acak (A-Z)
#         LPAD(FLOOR(RAND() * 9999) + 1, 4, '0')  -- Nomor acak (1-9999)
#     )
# );


# Install library MySQL:
# pip install mysql.connector

# import library 
import mysql.connector # library untuk menghubungkan kedalam database
import time # Library untuk waktu
import getpass # Library untuk password
import os # Library untuk berinteraksi dengan OS

# Function untuk clear terminal
def clear(): 
    if os.name == 'nt':  # Identitas OS windows
        os.system('cls')  # Sintaks windows untuk membersihkan layar terminal
    else:
        os.system('clear') # Sintaks untuk OS Unix membersihkan layar terminal
        
# Function untuk membuat koneksi kedalam database
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
        clear() # Function clear
        
# Function untuk user login
def login(username, password): 
    try: # Mencoba untuk fetch data sesuai dengan yang diinput oleh user (jika data True)
        db = db_connection() # Mendeklarasikan variable untuk function db_connection
        cursor = db.cursor() # Membuat cursor kedalam SQL
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password)) # Cursor mengeksekusi query untuk memilih column yang sesuai dengan yang diinput user berdasarkan parameter function
        get_user = cursor.fetchone() # Fetch 1 data dari kolom table
        if get_user: # Jika data berhasil di fetch
            clear() # Function clear
            print("\n\033[32m\033[1m!--Login Berhasil--!\033[0m\033[37m\n") # Alert keterangan untuk user
            time.sleep(1) # Membuat delay waktu selama 1 detik kepada terminal sebelum mengeksekusi sintaks selanjutnya
            clear() # Function clear
            main()  # Function main
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

# Function untuk menambah product baru
def add_new(name, category, weight, quantity, supplier):
    try: # Mencoba mengeksekusi 
        db = db_connection() # Mendeklarasikan variable untuk function db_connection
        cursor = db.cursor() # Membuat cursor kedalam SQL
        cursor.execute("SELECT * FROM tb_product WHERE name = %s AND weight = %s AND supplier = %s", (name, weight, supplier)) # Cursor mengeksekusi query untuk select semua column pada table
        cursor.fetchall() # Fetch semua data
        if cursor.rowcount == 0: # Jika produk yang ditambahkan belum ada pada column
            cursor.execute("INSERT INTO tb_product (name, category, weight, quantity, supplier) VALUES(%s, %s, %s, %s, %s)", (name, category, weight, quantity, supplier)) # Cursor mengeksekusi query untuk menambahkan produk kedalam database
            db.commit() # Menyimpan perubahan kedalam database
            print("\n\033[32m\033[1m!--Product Berhasil Ditambahkan--!\033[0m\033[37m\n") # Alert keterangan produk berhasil ditambahkan
            time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks berikutnya
            clear() # Function clear
        else: # Jika Produk sudah ada dalam database
            print(f"\033[31m\033[1m!--Gagal Menambah Product Baru--!\nProduct Sudah Ada\033[0m\033[37m") # Alert Keterangan produk gagal ditambahkan
            time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks berikutnya
            clear() # Function clear
            main() # Function main
    except ValueError as e: # Jika terdapat sintaks error pada try
        print(f"Error: {e}") 
        time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks selanjutnya
        clear() # Function clear
        main()
    finally: # Jika sudah selesai
        cursor.close() # Menutup cursor
        db.close() # Menutup koneksi kedatabase untuk menghemat memori

# Function +qty product
def update_qty(id, name, quantity, weight, supplier):
    try: # Mencoba mengeksekusi
        db = db_connection() # Mendeklarasikan variable untuk function db_connection
        cursor = db.cursor() # Membuat cursor kedalam SQL
        cursor.execute("SELECT id FROM tb_product WHERE name = %s AND weight = %s AND supplier = %s", (name, weight, supplier)) # Cursor mengeksekusi query untuk memilih column id berdasarkan name, weight, dan supplier
        select = cursor.fetchone() # Fetch 1 data yang match
        if select: # Jika select true
            cursor.execute("UPDATE tb_product SET quantity = quantity + %s WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (quantity, id, name, weight, supplier)) # Cursor mengeksekusi query untuk + quantity 
            db.commit() # Menyimpan perubahan kedalam database
            print("\n\033[32m\033[1m!--Berhasil Menambahkan Jumlah Product--!\033[0m\033[37m\n") # Alert keterangan berhasil menambahkan jumlah produk
            time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks selanjutnya
            clear() # Function clear
        else: # Jika select false
            print(f"\n\033[31m\033[1m!--Gagal Menambah Jumlah Product--!\033[0m\033[37m\n") # Alert keterangan gagal menambah jumlah produk
            time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks selanjutnya
            clear() # Function clear
    except ValueError as e: # Jika terdapat error pada try
        print(f"Error: {e}")
    finally: # Jika selesai 
        cursor.close() # Menutup cursor
        db.close() # Menutup koneksi untuk menghemat memori

# Function untuk - quantity
def reduce_qty(id, name, quantity, weight, supplier):
    try: # Mencoba mengeksekusi
        db = db_connection() # Mendeklarasikan variable untuk function db_connection
        cursor = db.cursor() # Membuat cursor pada SQL
        cursor.execute("SELECT id FROM tb_product WHERE name = %s AND weight = %s AND supplier = %s", (name, weight, supplier)) # Cursor mengeksekusi query untuk memilih column id berdasarkan name, weight, supplier
        select = cursor.fetchone() # Fetch 1 data yang macth
        if select: # Jika select true
            cursor.execute("UPDATE tb_product SET quantity = quantity - %s WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (quantity, id, name, weight, supplier)) # Cursor mengeksekusi query untuk mengurangi quantity
            db.commit() # Menyimpan perubahan kedalam SQL
            print("\n\033[32m\033[1m!--Berhasil Mengurangi Jumlah Product--!\033[0m\033[37m\n") # Alert keterangan berhasil mengurangi jumlah produk
            time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks selanjutnya
            clear() # Function clear
        else: # Jika select false
            print(f"\n\033[31m\033[1m!--Gagal Mengurangi Jumlah Product--!\033[0m\033[37m\n") # Alert keterangan gagal mengurangi jumlah produk
            time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks selanjutnya
            clear() # Function clear
    except ValueError as e: # Jika terdapat error pada try
        print(f"Error: {e}")        
    finally: # Jika selesai
        cursor.close() # Menutup cursor
        db.close() # Menutup koneksi untuk menghemat memori

# Function untuk menghapus produk
def remove_product(id, name, weight, supplier):
    try: # Mencoba mengeksekusi
        db = db_connection() # Mendeklarasikan variable untuk function db_connection
        cursor = db.cursor() # Membuat cursor pada SQL
        cursor.execute("SELECT * FROM tb_product WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (id, name, weight, supplier)) # Cursor mengeksekusi query untuk menghapus produk sesuai dengan id, name, weight, dan supplier
        select = cursor.fetchone() # Fetch data yang sesuai
        if select:
            cursor.execute("DELETE FROM tb_product WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (id, name, weight, supplier))
            db.commit()
            print("\n\033[32m\033[1m!--Product berhasil dihapus--!\033[0m\033[37m\n") # Alert keterangan produk berhasil dihapus
            time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks selanjutnya
            clear() # Function clear
        else:
            print(f"\033[31m\033[1m!--Gagal Menghapus Product--!\n\033[0m\033[37m") # Alert keterangan gagal menghapus produk
            time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks selanjutnya
            clear() # Function clear
    except ValueError as e: # Jika terdapat error pada try
        print(f"Error: {e}")
    finally: # Jika selesai
        cursor.close() # Menutup cursor
        db.close() # Menutup koneksi untuk menghemat memori

# Function melihat semua produk
def show_all():
    try: # Mencoba mengeksekusi
        db = db_connection() # Mendeklarasikan variable untuk function db_connection
        cursor = db.cursor() # Membuat cursor pada SQL
        cursor.execute("SELECT * FROM tb_product") # Cursor mengeksekusi query untuk select semua column
        show_result = cursor.fetchall() # Fetch semua data
        # Format untuk output
        print("--- DAFTAR PRODUK ---".center(100)) 
        print("="*100)
        print(f"{'ID':<5} {'Name':<25} {'Categpry':<20} {'Weight':<10} {'Quantity':<10} {'Supplier':<20}") # Membuat table dengan format lebar colomn
        print("="*100)
        for cell in show_result: # looping data sesuai dengan jumlah rows di database
            print(f"{cell[0]:<5} {cell[1]:<25} {cell[2]:<20} {cell[3]:<10} {cell[4]:<10} {cell[5]:<20}") # Membuat table dengan format cell sesuai dengan database
        print("="*100)
        answer = input("Kembali ke manu? ")
        if answer:
            time.sleep(2)
            clear()
            main()    
    except ValueError as e: # Jika terdapat error pada try
        print(f"Error: {e}")
    finally: # Jika selesai
        cursor.close() # Menutup cursor
        db.close() # Menutup koneksi untuk menghemat memori

# Function main(utama)
def main():
    while True: # Jika login berhasil / True
        print("\n\033[35m\033[1mSelamat Datang Di Minimarket\033[0m\033[37m\n")
        print("1. Tambah Product Baru")
        print("2. Update Jumlah Product")
        print("3. Hapus Product")
        print("4. Lihat Semua Product")
        print("5. Keluar")
        user_answer = int(input("Masukkan pilihan kamu(1/2/3/4/5): ")) # Variable untuk menampung jawaban user
        if user_answer == 1: # Jika user menginput 1
            clear() # Function clear
            print("Menambahkan  Product Baru\n")
            nama_product = input("Nama Product: ")
            catg_product = input("Kategoti Product: ")
            weig_product = int(input(("Berat Product(gram): ")))
            qtyy_product = int(input(("Jumlah Product: ")))
            splr_product = input("Supplier Product: ")
            add_new(nama_product, catg_product, weig_product, qtyy_product, splr_product) # Menjalankan function add_new dengan format 
        elif user_answer == 2: # Jika user menginput 2
            clear() # Function clear
            print("1. Tambahi Jumlah Product ")
            print("2. Kurangi Jumlah Product ")
            upd_user_answer = int(input("Masukkan pilihan kamu(1/2): ")) # Variable untuk menampung jawaban user
            if upd_user_answer == 1: # Jika user menginput 1
                clear() # Function clear
                print("Menambah Jumlah Product\n")
                frId_product = int(input("ID Product: "))
                nama_product = input("Nama Product: ")
                weig_product = int(input("Berat Product(gram): "))
                splr_product = input("Supplier Product: ")
                qtyy_product = int(input("Tambah Jumlah Product: "))
                update_qty(frId_product, nama_product, qtyy_product, weig_product, splr_product) # Menjalankan function update_qty dengan format
            elif upd_user_answer == 2: # Jika user menginput 2
                clear() # Function clear
                print("Mengurangi Jumlah Product\n")
                frId_product = int(input("ID Product: "))
                nama_product = input("Nama Product: ")
                weig_product = int(input("Berat Product(gram): "))
                splr_product = input("Supplier Product: ")
                qtyy_product = int(input("Tambah Jumlah Product: "))
                reduce_qty(frId_product, nama_product, qtyy_product, weig_product, splr_product) # Menjalankan function reduce_qty dengan format
            else: # Jika jawaban tidak valid
                clear() # Clear
                print("\033[31mJawaban tidak valid !\033[37m") # Alert keterangan jawaban tidak valid
                time.sleep(2) # Membuat delay selama 2 detik sebelum mengeksekusi sintaks selanjutnya
                clear() # Function clear
        elif user_answer == 3: # Jika user menginput 3
            clear() # Function clear
            print("Menghapus Product\n")
            frId_product = int(input("ID Product: "))
            nama_product = input("Nama Product: ")
            weig_product = int(input("Berat Product(gram): "))
            splr_product = input("Supplier Product: ")
            remove_product(frId_product, nama_product, weig_product, splr_product) # Menjalankan function remove_product dengan format    
        elif user_answer == 4: # Jika user menginput 4
            clear()
            show_all() # Menjalankan function show_all
        elif user_answer == 5: # Jika user menginput 5
            clear()
            print("\033[31mKeluar dari Aplikasi !\033[37m")
            time.sleep(2)
            clear()
            break # menghentikan function main
        else: # Jika jawaban tidak valid
            clear() # Function clear
            print("\033[31mJawaban tidak valid !\033[37m") # Alert keterangan jawaban tidak valid
            clear() # Function clear

# if __name__ == "__main__":
clear() # Function clear
while True: # looping login jika gagal maka akan terus loop sampai meminta agar login berhasil
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    login(username, password) # Menjalankan function login dengan format
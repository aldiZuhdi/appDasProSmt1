# import library 
import mysql.connector
import time
import getpass
import os

def clear(): 
    if os.name == 'nt':  
        os.system('cls') 
    else:
        os.system('clear') 
         
def db_connection():
    try:
        return mysql.connector.connect( 
            host = 'localhost', 
            user = 'root', 
            password = '', 
            database = 'db_minimarket' 
        )  
    except mysql.connector.Error as e: #
        print(f"Error: {e}") 
        

def login(username, password): 
    try:
        db = db_connection() 
        cursor = db.cursor() 
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password)) 
        get_user = cursor.fetchone() 
        if get_user: 
            clear() 
            print("\n\033[32m\033[1m!--Login Berhasil--!\033[0m\033[30m\n")
            time.sleep(1) 
            clear()
            main() 
        else:
            clear()
            print("\n\033[31m\033[1m!--Login Gagal--!\nusername atau password salah\033[0m\033[30m\n")
            time.sleep(1)
            clear()
    except ValueError as e:
        print(f"Error: {e}")   
    finally:
        cursor.close()
        db.close()

def add_new(name, category, weight, quantity, supplier):
    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_product WHERE name = %s AND weight = %s AND supplier = %s", (name, weight, supplier))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO tb_product (name, category, weight, quantity, supplier) VALUES(%s, %s, %s, %s, %s)", (name, category, weight, quantity, supplier))
            db.commit()
            print("\n\033[32m\033[1m!--Product Berhasil Ditambahkan--!\033[0m\033[30m\n")
            time.sleep(2)
            clear()
        else:
            print(f"\033[31m\033[1m!--Gagal Menambah Product Baru--!\nProduct Sudah Ada\033[0m\033[30m")
            time.sleep(2)
            clear()
            main()
    except ValueError as e:
        print(f"Error: {e}")
        time.sleep(2)
        clear()
    finally:
        cursor.close()
        db.close()

def update_qty(id, name, quantity, weight, supplier):
    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM tb_product WHERE name = %s AND weight = %s AND supplier = %s", (name, weight, supplier))
        select = cursor.fetchone()
        if select:
            cursor.execute("UPDATE tb_product SET quantity = quantity + %s WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (quantity, id, name, weight, supplier))
            db.commit()
            print("\n\033[32m\033[1m!--Berhasil Menambahkan Jumlah Product--!\033[0m\033[30m\n")
            time.sleep(2)
            clear()
        else:
            print(f"\n\033[31m\033[1m!--Gagal Menambah Jumlah Product--!\033[0m\033[30m\n")
            time.sleep(2)
            clear()
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def reduce_qty(id, name, quantity, weight, supplier):
    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM tb_product WHERE name = %s AND weight = %s AND supplier = %s", (name, weight, supplier))
        select = cursor.fetchone()
        if select:
            cursor.execute("UPDATE tb_product SET quantity = quantity - %s WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (quantity, id, name, weight, supplier))
            db.commit()
            print("\n\033[32m\033[1m!--Berhasil Mengurangi Jumlah Product--!\033[0m\033[30m\n")
            time.sleep(2)
            clear()
        else:
            print(f"\n\033[31m\033[1m!--Gagal Mengurangi Jumlah Product--!\033[0m\033[30m\n")
            time.sleep(2)
            clear()
    except ValueError as e:
        print(f"Error: {e}")        
    finally:
        cursor.close()
        db.close()

def remove_product(id, name, weight, supplier):
    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM tb_product WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (id, name, weight, supplier))
        db.commit()
        print("\n\033[32m\033[1m!--Product berhasil dihapus--!\033[0m\033[30m\n")
        time.sleep(2)
        clear()
    except ValueError as e:
        print(f"\033[31m\033[1m!--Gagal Menghapus Product--!\nError: {e}\033[0m\033[30m")
        time.sleep(2)
        clear()
    finally:
        cursor.close()
        db.close()

def show_all():
    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_product")
        show_result = cursor.fetchall()
        print("Daftar Produk:")
        print("="*100)
        print(f"{'ID':<5} {'Name':<25} {'Categpry':<20} {'Weight':<10} {'Quantity':<10} {'Supplier':<20}")
        print("="*100)
        for cell in show_result:
            print(f"{cell[0]:<5} {cell[1]:<25} {cell[2]:<20} {cell[3]:<10} {cell[4]:<10} {cell[5]:<20}")
        print("="*100)
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def main():
    while True:
        print("\n\033[35m\033[1mSelamat Datang Di Minimarket\033[0m\033[30m\n")
        print("1. Tambah Product Baru")
        print("2. Update Jumlah Product")
        print("3. Hapus Product")
        print("4. Lihat Semua Product")
        print("5. Keluar")
        user_answer = int(input("Masukkan pilihan kamu(1/2/3/4/5): "))
        if user_answer == 1:
            clear()
            print("Menambahkan  Product Baru\n")
            nama_product = input("Nama Product: ")
            catg_product = input("Kategoti Product: ")
            weig_product = int(input(("Berat Product(gram): ")))
            qtyy_product = int(input(("Jumlah Product: ")))
            splr_product = input("Supplier Product: ")
            add_new(nama_product, catg_product, weig_product, qtyy_product, splr_product)
        elif user_answer == 2:
            clear()
            print("1. Tambahi Jumlah Product: ")
            print("2. Kurangi Jumlah Product: ")
            upd_user_answer = int(input("Masukkan pilihan kamu(1/2): "))
            if upd_user_answer == 1:
                clear()
                print("Menambah Jumlah Product\n")
                frId_product = int(input("ID Product: "))
                nama_product = input("Nama Product: ")
                weig_product = int(input("Berat Product(gram): "))
                splr_product = input("Supplier Product: ")
                qtyy_product = int(input("Tambah Jumlah Product: "))
                update_qty(frId_product, nama_product, qtyy_product, weig_product, splr_product)
            elif upd_user_answer == 2:
                clear()
                print("Mengurangi Jumlah Product\n")
                frId_product = int(input("ID Product: "))
                nama_product = input("Nama Product: ")
                weig_product = int(input("Berat Product(gram): "))
                splr_product = input("Supplier Product: ")
                qtyy_product = int(input("Tambah Jumlah Product: "))
                reduce_qty(frId_product, nama_product, qtyy_product, weig_product, splr_product)
            else:
                clear()
                print("\033[31mJawaban tidak valid !\033[30m")
                clear()
        elif user_answer == 3:
            clear()
            print("Menghapus Product\n")
            frId_product = int(input("ID Product: "))
            nama_product = input("Nama Product: ")
            weig_product = int(input("Berat Product(gram): "))
            splr_product = input("Supplier Product: ")
            remove_product(frId_product, nama_product, weig_product, splr_product)    
        elif user_answer == 4:
            show_all()
        elif user_answer == 5:
            break
        else:
            clear()
            print("\033[31mJawaban tidak valid !\033[30m")
            clear()       

if __name__ == "__main__":
    clear()
    while True:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        login(username, password)
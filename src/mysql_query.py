import streamlit as web
import pandas as pd
from src.connection import connToDb
import time

conn = connToDb()

users = [
    {"username" : "admin",
     "password" : "admin"
     },
    {"username" : "aldi",
     "password" : "aldi"
     },
]
def add_new(name, category, weight, quantity, supplier, addOn, updateOn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE name = %s AND weight = %s AND supplier = %s", (name, weight, supplier))
    cursor.fetchall()
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO tb_product (name, category, weight, quantity, supplier, add_on, update_on) VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, category, weight, quantity, supplier, addOn, updateOn))
        conn.commit()
        web.success("Produk berhasil ditambahkan!")
        time.sleep(1)
        web.rerun()
    else:
        web.error("Produk baru yang ingin ditambahkan sudah ada!")
        
def update_qty(id, quantity, updateOn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE id = %s", (id,))
    select = cursor.fetchone()
    if select:
        cursor.execute("UPDATE tb_product SET quantity = quantity + %s, update_on = %s WHERE id = %s", (quantity, updateOn, id))
        conn.commit()
        web.success("Stok produk berhasil ditambah!")
        time.sleep(1)
        web.rerun()
    else:
        web.error("Produk yang ingin ditambah stoknya tidak ditemukan!")

def reduce_qty(id, quantity, updateOn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE id = %s", (id,))
    select = cursor.fetchone()
    if select:
        cursor.execute("UPDATE tb_product SET quantity = quantity - %s, update_on = %s WHERE id = %s", (quantity, updateOn, id))
        conn.commit()
        web.success("Stok produk berhasil dikurangi!")
        time.sleep(1)
        web.rerun()
    else:
        web.error("Produk yang ingin dikurangi stoknya tidak ditemukan!")
def remove_product(id, name, weight, supplier):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (id, name, weight, supplier))
    select = cursor.fetchone()
    if select:
        cursor.execute("DELETE FROM tb_product WHERE id = %s AND name = %s AND weight = %s AND supplier = %s", (id, name, weight, supplier))
        conn.commit()
        web.success("Produk berhasil dihapus!")
        time.sleep(1)
        web.rerun()
    else:
        web.error("Produk yang ingin dihapus tidak ditemukan!")
        
def show_all():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_product")
    result = cursor.fetchall()
    tb_product = pd.DataFrame(result, columns=["ID", "NAME", "CATEGORY", "WEIGHT", "QUANTITY", "SUPPLIER", "DITAMBAHKAN PADA", "DIUPDATE PADA"])
    def low_stok(row):
        if row['QUANTITY'] < 50:
            return['background-color: #fce1e1; color: #000000'] * len(row)
        elif row['QUANTITY'] > 50 or row['QUANTITY'] == 50:
            return ['background-color: #e4fce1; color: #000000'] * len(row)
        else:
            return [''] * len(row)
    style_low_stok = tb_product.style.apply(low_stok, axis = 1)
    return style_low_stok
def show_by_name(name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE name = %s", (name,))
    result = cursor.fetchall()
    tb_product = pd.DataFrame(result, columns=["ID", "NAME", "CATEGORY", "WEIGHT", "QUANTITY", "SUPPLIER", "DITAMBAHKAN PADA", "DIUPDATE PADA"]) 
    def low_stok(row):
        if row['QUANTITY'] < 50:
            return['background-color: #fce1e1; color: #000000'] * len(row)
        elif row['QUANTITY'] > 50 or row['QUANTITY'] == 50:
            return ['background-color: #e4fce1; color: #000000'] * len(row)
        else:
            return [''] * len(row)
    style_low_stok = tb_product.style.apply(low_stok, axis = 1)
    return style_low_stok

def show_by_category(category):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE category = %s", (category,))
    result = cursor.fetchall()
    tb_product = pd.DataFrame(result, columns=["ID", "NAME", "CATEGORY", "WEIGHT", "QUANTITY", "SUPPLIER", "DITAMBAHKAN PADA", "DIUPDATE PADA"])
    def low_stok(row):
        if row['QUANTITY'] < 50:
            return ['background-color: #fce1e1; color: #000000'] * len(row)
        elif row['QUANTITY'] > 50 or row['QUANTITY'] == 50:
            return ['background-color: #e4fce1; color: #000000'] * len(row)
        else:
            return [''] * len(row)
    style_low_stok = tb_product.style.apply(low_stok, axis = 1)
    return style_low_stok

def show_by_lowStok():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE quantity < 50")
    result = cursor.fetchall()
    tb_product = pd.DataFrame(result, columns=["ID", "NAME", "CATEGORY", "WEIGHT", "QUANTITY", "SUPPLIER", "DITAMBAHKAN PADA", "DIUPDATE PADA"])
    def low_stok(row):
        if row['QUANTITY'] < 50:
            return ['background-color: #fce1e1; color: #000000'] * len(row)
        elif row['QUANTITY'] > 50 or row['QUANTITY'] == 50:
            return ['background-color: #e4fce1; color: #000000'] * len(row)
        else:
            return [''] * len(row)
    style_low_stok = tb_product.style.apply(low_stok, axis = 1)
    return style_low_stok

def SQLlogin(username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    fetch = cursor.fetchone()
    if fetch:
        web.success("Login Berhasil")
        web.experimental_rerun()
    else:
        web.error("Username atau Password Salah")
    
    
def loginVerification(username, password):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False
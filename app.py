# pip install mysql.connector
# pip install streamlit
# pip install pandas

# import library
import mysql.connector as db
import streamlit as web
import pandas as pd
from src.connection import connToDb 
from src.mysql_query import add_new, update_qty, reduce_qty, remove_product, show_all, show_by_name, loginVerification

# Koneksi kedalam database

conn = connToDb()

# Front End
if "logged_in" not in web.session_state:
    web.session_state.logged_in = False
    web.session_state.username = ""
if not web.session_state.logged_in:
    web.title("Silahkan Login")
    username = web.text_input("Username:", placeholder = "Masukkan username", autocomplete = "off")
    password = web.text_input("Password:", placeholder = "Masukkan password", type = "password", autocomplete = "off")
    if web.button("Login"):
        if loginVerification(username, password):
            web.session_state.logged_in = True
            web.session_state.username = username
            web.success("Berhasil Login! tekan sekali lagi untuk masuk")
        else:
            web.error("username atau password salah")
else:
    web.title("STOK BARANG AGEN PAK MAHMUD")
    searchBar = web.text_input("Cari nama produk:", "", autocomplete = "off", placeholder = "Cari nama produk sesuai dengan kolom NAME pada tabel")
    if searchBar:
        sbn_result = show_by_name(searchBar)
        if sbn_result is not None:
            web.dataframe(sbn_result)
    else:
        web.subheader("Data Produk:")
        sa_result = show_all()
        web.dataframe(sa_result) 
        if web.sidebar.button("Logout"):
            web.session_state.logged_in = False
            web.session_state.username = ""
            web.sidebar.success("Berhasil Logout! tekan sekali lagi untuk keluar")
        web.sidebar.title(f"Halo, {web.session_state.username}")
        selectBox = web.sidebar.selectbox("Lakukan sesuatu:", ["Tambah Produk Baru", "Tambahi Jumlah Produk", "Kurangi Jumlah Produk", "Hapus Produk"], index = 0)
        if selectBox == "Tambah Produk Baru":
            web.sidebar.title("Tambah Produk Baru")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            category = web.sidebar.selectbox("Kategori Produk", ["Penyedap/bumbu dapur", "Bahan Pangan/Pokok", "Minuman Kemasan/Sachet", "Perlengkapan Rumah Tangga", "Kamar Mandi & Mencuci"])
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Tambahkan"):
                add_new(name, category, weight, quantity, supplier)
        elif selectBox == "Tambahi Jumlah Produk":
            web.sidebar.title("Menambah Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Tambah Qty"):
                update_qty(id, name, quantity, weight, supplier)
        elif selectBox == "Kurangi Jumlah Produk":
            web.sidebar.title("Mengurangi Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Kurangi Qty"):
                reduce_qty(id, name, quantity, weight, supplier)
        elif selectBox == "Hapus Produk":
            web.sidebar.title("Hapus Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Hapus"):
                remove_product(id, name, weight, supplier)
    
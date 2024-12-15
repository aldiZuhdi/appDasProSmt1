# pip install mysql.connector
# pip install streamlit
# pip install pandas

# import library
import streamlit as web
from src.connection import connToDb 
from src.mysql_query import add_new, update_qty, reduce_qty, remove_product, show_all, show_by_name, loginVerification, show_by_category, show_by_lowStok
import datetime

# Initialize variables
conn = connToDb() # Koneksi kedalam database
current_datetime = datetime.datetime.now() # Setup tanggal dan waktu
addOn = current_datetime.strftime('%Y-%m-%d %H:%M:%S') # Format tanggal dan waktu


# FRONT END

# Check user in session state
if "logged_in" not in web.session_state:
    web.session_state.logged_in = False
    web.session_state.username = ""

# If login data is available # Make user input form login
if not web.session_state.logged_in:
    web.title("Silahkan Login")
    username = web.text_input("Username:", placeholder = "Masukkan username", autocomplete = "off")
    password = web.text_input("Password:", placeholder = "Masukkan password", type = "password", autocomplete = "off")
    # If button onClick
    if web.button("Login"):
        # If text_input is not empty
        if username and password:
            if loginVerification(username, password):
                web.session_state.logged_in = True
                web.session_state.username = username
                web.success("Berhasil Login! tekan sekali lagi untuk masuk")
            else:
                web.error("username atau password salah")
        else:
            web.error("Username dan Password harus diisi!")

# Dashboard App
else:
    web.title("STOK BARANG AGEN PAK MAHMUD")
    search = web.selectbox("Cari berdasarkan:", ["Beranda", "Berdasarkan nama", "Berdasarkan kategori", "Berdasarkan stok hampir habis"])
    if search == "Berdasarkan nama":
        searchBar = web.text_input("Cari nama produk:", autocomplete = "off", placeholder = "Cari nama produk sesuai dengan kolom NAME pada tabel")
        if searchBar:
            sbn_result = show_by_name(searchBar)
            if sbn_result:
                web.dataframe(sbn_result)
        else:
            sa = show_all()
            web.dataframe(sa)
        if web.sidebar.button("Logout"):
            web.session_state.logged_in = False
            web.session_state.username = ""
            web.sidebar.success("Berhasil Logout! tekan sekali lagi untuk keluar")
        web.sidebar.title(f"Halo, {web.session_state.username}")
        selectBox = web.sidebar.selectbox("Lakukan sesuatu:", ["Tambah Produk Baru", "Tambah Jumlah Produk", "Kurang Jumlah Produk", "Hapus Produk"], index = 0)
        if selectBox == "Tambah Produk Baru":
            web.sidebar.title("Tambah Produk Baru")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            category = web.sidebar.selectbox("Kategori Produk", ["Bumbu dapur", "Bahan Pokok", "Minuman Kemasan/Sachet", "Makanan ringan", "Perlengkapan mandi/mencuci", "Perlengkapan rumah tangga", "Kebutuhan lainnya"])
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Tambahkan"):
                if name and category and weight and quantity and supplier:
                    add_new(name, category, weight, quantity, supplier, addOn, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Tambah Jumlah Produk":
            web.sidebar.title("Menambah Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Tambah Qty"):
                if id and quantity:
                    update_qty(id, quantity, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Kurang Jumlah Produk":
            web.sidebar.title("Mengurangi Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Kurangi Qty"):
                if id and quantity:
                    reduce_qty(id, quantity, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Hapus Produk":
            web.sidebar.title("Hapus Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Hapus"):
                if id and name and weight and supplier:
                    remove_product(id, name, weight, supplier)
                else:
                    web.error("Form tidak boleh kosong!")
        
    elif search == "Berdasarkan kategori":
        searchBar = web.selectbox("Cari kategori produk", ["Bumbu dapur", "Bahan Pokok", "Minuman Kemasan/Sachet", "Makanan ringan", "Perlengkapan mandi/mencuci", "Perlengkapan rumah tangga", "Kebutuhan lainnya"])
        web.title("DATA PRODUK KATEGORI")
        if searchBar:
            sbk_result = show_by_category(searchBar)
            if sbk_result is not None:
                web.dataframe(sbk_result)
        if web.sidebar.button("Logout"):
            web.session_state.logged_in = False
            web.session_state.username = ""
            web.sidebar.success("Berhasil Logout! tekan sekali lagi untuk keluar")
        web.sidebar.title(f"Halo, {web.session_state.username}")
        selectBox = web.sidebar.selectbox("Lakukan sesuatu:", ["Tambah Produk Baru", "Tambah Jumlah Produk", "Kurang Jumlah Produk", "Hapus Produk"], index = 0)
        if selectBox == "Tambah Produk Baru":
            web.sidebar.title("Tambah Produk Baru")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            category = web.sidebar.selectbox("Kategori Produk", ["Bumbu dapur", "Bahan Pokok", "Minuman Kemasan/Sachet", "Makanan ringan", "Perlengkapan mandi/mencuci", "Perlengkapan rumah tangga", "Kebutuhan lainnya"])
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Tambahkan"):
                if name and category and weight and quantity and supplier:
                    add_new(name, category, weight, quantity, supplier, addOn, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Tambah Jumlah Produk":
            web.sidebar.title("Menambah Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Tambah Qty"):
                if id and quantity:
                    update_qty(id, quantity, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Kurang Jumlah Produk":
            web.sidebar.title("Mengurangi Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Kurangi Qty"):
                if id and quantity:
                    reduce_qty(id, quantity, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Hapus Produk":
            web.sidebar.title("Hapus Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Hapus"):
                if id and name and weight and supplier:
                    remove_product(id, name, weight, supplier)
                else:
                    web.error("Form tidak boleh kosong!")
                    
    elif search == "Berdasarkan stok hampir habis":
        web.title("DATA PRODUK LOW STOK")
        sbls_result = show_by_lowStok()
        web.dataframe(sbls_result)
        if web.sidebar.button("Logout"):
            web.session_state.logged_in = False
            web.session_state.username = ""
            web.sidebar.success("Berhasil Logout! tekan sekali lagi untuk keluar")
        web.sidebar.title(f"Halo, {web.session_state.username}")
        selectBox = web.sidebar.selectbox("Lakukan sesuatu:", ["Tambah Produk Baru", "Tambah Jumlah Produk", "Kurang Jumlah Produk", "Hapus Produk"], index = 0)
        if selectBox == "Tambah Produk Baru":
            web.sidebar.title("Tambah Produk Baru")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            category = web.sidebar.selectbox("Kategori Produk", ["Bumbu dapur", "Bahan Pokok", "Minuman Kemasan/Sachet", "Makanan ringan", "Perlengkapan mandi/mencuci", "Perlengkapan rumah tangga", "Kebutuhan lainnya"])
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Tambahkan"):
                if name and category and weight and quantity and supplier:
                    add_new(name, category, weight, quantity, supplier, addOn, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Tambah Jumlah Produk":
            web.sidebar.title("Menambah Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Tambah Qty"):
                if id and quantity:
                    update_qty(id, quantity, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Kurang Jumlah Produk":
            web.sidebar.title("Mengurangi Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Kurangi Qty"):
                if id and quantity:
                    reduce_qty(id, quantity, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Hapus Produk":
            web.sidebar.title("Hapus Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Hapus"):
                if id and name and weight and supplier:
                    remove_product(id, name, weight, supplier)
                else:
                    web.error("Form tidak boleh kosong!")
    # searchBar = web.text_input("Cari nama produk:", autocomplete = "off", placeholder = "Cari nama produk sesuai dengan kolom NAME pada tabel")
    # if searchBar:
    #     sbn_result = show_by_name(searchBar)
    #     if sbn_result is not None:
    #         web.dataframe(sbn_result)
    else:
        web.subheader("Data Produk")
        sa_result = show_all()
        web.dataframe(sa_result) 
        if web.sidebar.button("Logout"):
            web.session_state.logged_in = False
            web.session_state.username = ""
            web.sidebar.success("Berhasil Logout! tekan sekali lagi untuk keluar")
        web.sidebar.title(f"Halo, {web.session_state.username}")
        selectBox = web.sidebar.selectbox("Lakukan sesuatu:", ["Tambah Produk Baru", "Tambah Jumlah Produk", "Kurang Jumlah Produk", "Hapus Produk"], index = 0)
        if selectBox == "Tambah Produk Baru":
            web.sidebar.title("Tambah Produk Baru")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            category = web.sidebar.selectbox("Kategori Produk", ["Bumbu dapur", "Bahan Pokok", "Minuman Kemasan/Sachet", "Makanan ringan", "Perlengkapan mandi/mencuci", "Perlengkapan rumah tangga", "Kebutuhan lainnya"])
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Tambahkan"):
                if name and category and weight and quantity and supplier:
                    add_new(name, category, weight, quantity, supplier, addOn, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
        elif selectBox == "Tambah Jumlah Produk":
            web.sidebar.title("Menambah Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Tambah Qty"):
                if id and quantity:
                    update_qty(id, quantity, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                
        elif selectBox == "Kurang Jumlah Produk":
            web.sidebar.title("Mengurangi Jumlah Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            quantity = web.sidebar.text_input("Jumlah Produk (pcs)", autocomplete = "off")
            if web.sidebar.button("Kurangi Qty"):
                if id and quantity:
                    reduce_qty(id, quantity, addOn)
                else:
                    web.error("Form tidak boleh kosong!")
                    
        elif selectBox == "Hapus Produk":
            web.sidebar.title("Hapus Produk")
            id = web.sidebar.text_input("ID Produk", autocomplete = "off")
            name = web.sidebar.text_input("Nama Produk", autocomplete = "off")
            weight = web.sidebar.text_input("Berat Produk", autocomplete = "off")
            supplier = web.sidebar.text_input("Supplier", autocomplete = "off")
            if web.sidebar.button("Hapus"):
                if id and name and weight and supplier:
                    remove_product(id, name, weight, supplier)
                else:
                    web.error("Form tidak boleh kosong!")
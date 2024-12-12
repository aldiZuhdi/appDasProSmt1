import streamlit as web
import time
import pandas as pd
import mysql.connector

# Fungsi untuk koneksi ke database
def connToDb():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_minimarket'
    )

# Koneksi ke database
conn = connToDb()

# Data pengguna dummy
users = [
    {
        "username": "admin",
        "password": "admin",
        "position": "admin"
    },
    {
        "username": "aldi",
        "password": "aldi",
        "position": "user"
    }
]

# Fungsi untuk login dan menuju dashboard
def loginQuery(username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    select = cursor.fetchone()
    if select:
        # Jika login berhasil, set status login di session_state
        web.session_state.logged_in = True
        web.session_state.username = username
        dashboard()
    else:
        web.error("Username atau Password salah!")

# Fungsi untuk registrasi pengguna
def registerQuery(username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    cursor.fetchall()
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        web.success("Registrasi berhasil!")
    else:
        web.error("Username sudah digunakan, silahkan pilih username yang lain.")

# Form untuk registrasi
def registerForm():
    username = web.text_input("Username:")
    password = web.text_input("Password:")
    if web.button("Register"):
        registerQuery(username, password)

# Form untuk login
def loginForm():
    # Mengecek apakah user sudah login
    if 'logged_in' in web.session_state and web.session_state.logged_in:
        # Jika sudah login, langsung tampilkan dashboard
        dashboard()
        return
    
    username = web.text_input("Buat username:")
    password = web.text_input("Buat password:", type="password")
    web.text("Tidak memiliki akun?")
    
    if web.button("Register Now"):
        registerForm()

    if web.button("Login"):
        loginQuery(username, password)

# Halaman dashboard
def dashboard():
    web.title("Dashboard")
    if 'username' in web.session_state:
        web.write(f"Selamat datang, {web.session_state.username}!")
    
    # Tombol Logout
    if web.button("Logout"):
        web.session_state.logged_in = False
        web.session_state.username = None
        web.experimental_rerun()  # Meng-refresh halaman untuk kembali ke form login

# Program utama
if __name__ == "__main__":
    loginForm()

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Daftar ID dan password admin
admin_users = {
    "admin1": {"password": "123", "name": "Admin1"},
    "admin2": {"password": "456", "name": "Admin2"}
}

# Daftar karyawan dengan NIP dan nama
karyawan_data = {
    "19241461": "Dzulfiqar Dumaid",
    "19240679": "Fahri Akbar Indratama",
    "19242263": "Muhammad Adita Ramadhani",
    "19240646": "Muhammad Galang Nur Falsian",
    "19241045": "Rifdah Rohadatul Aisy",
}

# Fungsi untuk login admin
def login(username, password):
    user = admin_users.get(username)
    if user and user["password"] == password:
        return user["name"]  # Kembalikan nama pengguna jika login berhasil
    return None

# Cek apakah admin sudah login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.admin_name = ""

# Fungsi untuk login admin saat tombol diklik
def handle_login():
    admin_name = login(st.session_state["username"], st.session_state["password"])
    if admin_name:
        st.session_state.logged_in = True
        st.session_state.admin_name = admin_name
        st.success(f"Selamat datang, {st.session_state.admin_name}!")
    else:
        st.error("ID Admin atau password salah!")



# Jika admin belum login, tampilkan form login
if not st.session_state.logged_in:
    st.title("Login Admin")
    with st.form(key="login_form"):
        username = st.text_input("Masukkan ID Admin", key="username")
        password_input = st.text_input("Masukkan Password", type="password", key="password")
        login_button = st.form_submit_button("Login", on_click=handle_login)
        if login_button:
            handle_login()

# Setelah login, proses penghitungan gaji
else:
    st.title("Penghitungan Gaji Pegawai Negeri Sipil dengan Tunjangan dan Pajak")

    # Input NIP karyawan
    nip_karyawan = st.text_input("Masukkan NIP Karyawan yang Terdaftar:")

    if nip_karyawan in karyawan_data:
        nama_karyawan = karyawan_data[nip_karyawan]
        st.success(f"Karyawan ditemukan: {nama_karyawan}")

        # Input gaji pokok hanya setelah NIP valid
        gaji_pokok = st.number_input("Masukkan Gaji Pokok Karyawan:", min_value=0.0, step=1000000.0, key="gaji_pokok")
        
        # Format Rupiah
        def format_rupiah(value):
            return "Rp {:,}".format(int(value)).replace(",", ".")
        
        if gaji_pokok > 0:
            st.write("Gaji Pokok:", format_rupiah(gaji_pokok))
        
        # Pilihan Golongan dan detail lainnya tetap seperti sebelumnya
        golongan = st.selectbox("Masukkan Golongan Karyawan:",
                                options=[None, "Golongan 1 (Lulusan SMP)", 
                                         "Golongan 2 (Lulusan SMA)", 
                                         "Golongan 3 (Lulusan D3/S1)", 
                                         "Golongan 4 (Lulusan S2)"],
                                format_func=lambda x: " " if x is None else x)
        
        status = st.selectbox("Apakah karyawan sudah menikah?",
                              options=[None, "Ya, sudah menikah", "Tidak, belum menikah"],
                              format_func=lambda x: " " if x is None else x)

        jumlah_anak = 0
        if status == "Ya, sudah menikah":
            jumlah_anak = st.selectbox("Berapa jumlah anak?",
                                       options=[None, "Belum punya anak", 1, 2, 3, "Lebih dari 3"],
                                       format_func=lambda x: " " if x is None else x)
        
        kendaraan = st.selectbox("Apakah karyawan memiliki kendaraan roda empat lebih dari 1?",
                                 options=[None, "Ya", "Tidak"],
                                 format_func=lambda x: " " if x is None else x)

        jam_kerja = st.number_input("Masukkan Jam Kerja: (lebih dari 60 jam mendapat upah lembur)",
                                    step=5, format="%d")
        
        if jam_kerja > 60:
            st.write(f"Karyawan mendapat upah lembur sebanyak {jam_kerja - 60} jam")

        hitung_button = st.button("Hitung Gaji")

        if hitung_button :
        # Pastikan input gaji_pokok diisi sebelum melanjutkan perhitungan
            if gaji_pokok > 0:
                # Perhitungan Tunjangan Berdasarkan Golongan
                tunjangan_golongan = 0
                if golongan == "Golongan 1 (Lulusan SMP)":
                    tunjangan_golongan = gaji_pokok * 0.05
                elif golongan == "Golongan 2 (Lulusan SMA)":
                    tunjangan_golongan = gaji_pokok * 0.10
                elif golongan == "Golongan 3 (Lulusan D3/S1)":
                    tunjangan_golongan = gaji_pokok * 0.15
                elif golongan == "Golongan 4 (Lulusan S2)":
                    tunjangan_golongan = gaji_pokok * 0.20

                # Perhitungan Tunjangan Keluarga dan PTKP (Penghasilan Tidak Kena Pajak)
                tunjangan_keluarga = 0
                if jumlah_anak == "Belum Punya Anak":
                    tunjangan_keluarga = gaji_pokok * 0.05
                elif jumlah_anak == 1:
                    tunjangan_keluarga = gaji_pokok * 0.10
                elif jumlah_anak == 2:
                    tunjangan_keluarga = gaji_pokok * 0.15
                elif jumlah_anak == 3:
                    tunjangan_keluarga = gaji_pokok * 0.20
                elif jumlah_anak == "Lebih dari 3":
                    tunjangan_keluarga = gaji_pokok * 0.25
                else :
                    tunjangan_keluarga = 0

                # Perhitungan Lembur
                lembur = 0
                if jam_kerja > 60:
                    lembur = (jam_kerja - 60) * 50000

                # Menghitung Gaji Total Sebelum Pajak
                gaji_total = gaji_pokok + tunjangan_golongan + tunjangan_keluarga + lembur

                # Mengitung Penghasilan Tidak Kena Pajak
                ptkp = 0
                if jumlah_anak == "Belum Punya Anak":
                    ptkp = ( (gaji_total * 12) - 50000000 ) / 12
                elif jumlah_anak == 1:
                    ptkp = ( (gaji_total * 12) - 60000000 ) / 12
                elif jumlah_anak == 2:
                    ptkp = ( (gaji_total * 12) - 65000000 ) / 12
                elif jumlah_anak == 3:
                    ptkp = ( (gaji_total * 12) - 70000000 ) / 12
                elif jumlah_anak == "Lebih dari 3":
                    ptkp = ( (gaji_total * 12) - 75000000 ) / 12
                else :
                    ptkp = ( (gaji_total * 12) - 40000000 ) / 12

                penghasilan_yang_kena_pajak = gaji_total  - ptkp
                
                #Mengitung Pajak Yang Dikenakan

                # PPH 21
                pph21 = 0
                if penghasilan_yang_kena_pajak * 12 <= 50000000 :
                    pph21 = penghasilan_yang_kena_pajak * 0.10
                elif penghasilan_yang_kena_pajak * 12 <= 60000000 :
                    pph21 = penghasilan_yang_kena_pajak * 0.20
                elif penghasilan_yang_kena_pajak * 12 <= 70000000 :
                    pph21 = penghasilan_yang_kena_pajak * 0.30
                elif penghasilan_yang_kena_pajak * 12 <= 80000000 :
                    pph21 = penghasilan_yang_kena_pajak * 0.35

                # PAJAK KENDARAAN
                pajak_kendaraan = penghasilan_yang_kena_pajak * 0.10 if kendaraan == "Ya" else 0

                # TAPERA
                tapera = penghasilan_yang_kena_pajak * 0.05

                # MENGHITUNG TOTAL PAJAK
                pajak = pph21 + pajak_kendaraan + tapera

                # MENGHITUNG GAJI TOTAL SETELAH KENA PAJAK
                gaji_setelah_pajak = gaji_total - pajak

            # Data hasil perhitungan
            result_data = {
                'Deskripsi': [
                    'Gaji Pokok', 
                    'Tunjangan Golongan', 
                    'Tunjangan Keluarga', 
                    'Tunjangan Lembur', 
                    'Total Gaji Sebelum Pajak', 
                    'Penghasilan Tidak Kena Pajak (PTKP)', 
                    'Total Gaji Yang Dipajak', 
                    'PPh 21', 
                    'Pajak Kendaraan', 
                    'Pajak TAPERA',
                    'Total Pajak',
                    'Total Gaji Setelah Pajak'
                ],
                'Jumlah': [
                    gaji_pokok, 
                    tunjangan_golongan, 
                    tunjangan_keluarga, 
                    lembur, 
                    gaji_total, 
                    ptkp, 
                    penghasilan_yang_kena_pajak,
                    pph21,
                    pajak_kendaraan, 
                    tapera,
                    pajak,
                    gaji_setelah_pajak
                ]
            }

            # Konversi ke DataFrame
            df_result = pd.DataFrame(result_data)

            # Format angka ke format rupiah
            df_result['Jumlah'] = df_result['Jumlah'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))

            # Menambahkan kolom 'No' mulai dari 1
            df_result['No'] = range(1, len(df_result) + 1)

            # Set kolom 'No' sebagai index
            df_result.set_index('No', inplace=True)

            # Data hasil perhitungan
            st.subheader(f"Hasil Perhitungan Gaji untuk {nama_karyawan}:")
            st.dataframe(df_result)

            # Pindahkan kolom 'No' ke depan dan hilangkan index default
            df_result = df_result[['Deskripsi', 'Jumlah']]

            # Menampilkan diagram pajak
            st.subheader("Diagram Pajak")
            components = {
                "Total Gaji": gaji_total,
                "PPh 21": pph21,
                "Pajak Kendaraan": pajak_kendaraan,
                "TAPERA": tapera,
            }
            labels = components.keys()
            sizes = components.values()
            colors = ["#66c2a5", "#8da0cb", "#e78ac3", "#e5c494"]
            explode = (0, 0.1, 0.1, 0.1)

            plt.figure(figsize=(7, 7))
            plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors, explode=explode)
            st.pyplot(plt)
        
                    # Tambahkan tombol ulang proses
            ulang_proses = st.button("Ulangi Proses")

            if ulang_proses:
                # Reset semua variabel ke nilai default
                st.session_state.nip_karyawan = ""
                st.session_state.gaji_pokok = 0
                st.session_state.golongan = None
                st.session_state.status = None
                st.session_state.jumlah_anak = None
                st.session_state.kendaraan = None
                st.session_state.jam_kerja = 0

                st.success("Proses telah diulang. Silakan masukkan NIP kembali.")
                st.experimental_rerun()  # Paksa aplikasi untuk refresh ke awal

            # Input NIP kembali
            nip_karyawan = st.text_input("Masukkan NIP Karyawan yang Terdaftar:", key="nip_karyawan")
            if nip_karyawan in karyawan_data:
                st.success(f"Karyawan ditemukan: {karyawan_data[nip_karyawan]}")
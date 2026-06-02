import streamlit as st
import pandas as pd

# Konfigurasi halaman agar melebar penuh (Wide Mode)
st.set_page_config(layout="wide", page_title="Logistics Graph App")

# ==========================================
# 🎨 CSS KUSTOM: TAMPILAN MODE APLIKASI
# ==========================================
def set_app_theme():
    st.markdown(
        """
        <style>
        /* Background Utama Aplikasi */
        .stApp {
            background-color: #f4f6f9;
        }
        
        /* Mengubah Font Utama */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
        
        /* Desain Kotak Kartu (Card) untuk Form & Data */
        div.custom-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            border: 1px solid #eef2f6;
        }
        
        /* Merapikan style tab di dalam aplikasi */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f8f9fa;
            border-radius: 6px 6px 0px 0px;
            padding: 10px 20px;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1e3d59 !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_app_theme()

# ==========================================
# 📦 STATE MANAGEMENT (Data Graph)
# ==========================================
if 'graph' not in st.session_state:
    st.session_state.graph = {
        "Jakarta": {"Bandung": 150, "Semarang": 450},
        "Bandung": {"Jakarta": 150, "Semarang": 370},
        "Semarang": {"Jakarta": 450, "Bandung": 370, "Surabaya": 350},
        "Surabaya": {"Semarang": 350}
    }

graph = st.session_state.graph

# ==========================================
# 📐 LAYOUT UTAMA APLIKASI
# ==========================================

# Top Bar / Header Aplikasi
st.markdown("<h1 style='color: #1e3d59; margin-bottom: 0;'>🚀 LOGIX - Rute Graph Navigator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #6c757d; margin-top: 0; margin-bottom: 25px;'>Sistem Manajemen Node & Jalur Distribusi Logistik Perusahaan</p>", unsafe_allow_html=True)

# Membagi layar menjadi 2 kolom: Kiri (Form CRUD) & Kanan (Monitor Data)
kolom_kontrol, kolom_monitor = st.columns([1, 1.2], gap="large")

# ------------------------------------------
# KOLOM KIRI: PANEL MANAGEMENT (CRUD FORM)
# ------------------------------------------
with kolom_kontrol:
    st.markdown("<h3 style='color: #1e3d59;'>⚙️ Panel Manajemen Rute</h3>", unsafe_allow_html=True)
    
    # Bungkus Menu Tab ke dalam bentuk komponen Aplikasi (Card)
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["➕ TAMBAH DATA", "🔄 UPDATE JARAK", "❌ HAPUS DATA"])
    
    # 1. Action: Create
    with tab1:
        st.write("##") # Spacer
        pilihan_input = st.radio("Pilih Jenis Data:", ["Titik Kota (Node)", "Rute Antar Kota (Edge)"], horizontal=True)
        
        if pilihan_input == "Titik Kota (Node)":
            kota_baru = st.text_input("Nama Kota Baru", placeholder="Masukkan nama kota...").strip()
            if st.button("Daftarkan Kota Ke Sistem", use_container_width=True):
                if kota_baru and kota_baru not in graph:
                    graph[kota_baru] = {}
                    st.success(f"Sukses: Kota {kota_baru} terdaftar.")
                    st.rerun()
                elif kota_baru in graph:
                    st.warning("Peringatan: Kota sudah ada di sistem.")
        
        else:
            daftar_kota = list(graph.keys())
            if len(daftar_kota) >= 2:
                asal = st.selectbox("Pilih Titik Asal", daftar_kota, key="c_asal")
                tujuan = st.selectbox("Pilih Titik Tujuan", daftar_kota, key="c_tuj")
                jarak = st.number_input("Estimasi Jarak Tempuh (km)", min_value=1, value=100)
                if st.button("Hubungkan Jalur Pengiriman", use_container_width=True):
                    if asal != tujuan:
                        graph[asal][tujuan] = jarak
                        graph[tujuan][asal] = jarak
                        st.success(f"Sukses: Jalur {asal} ↔️ {tujuan} aktif.")
                        st.rerun()
                    else:
                        st.error("Kesalahan: Titik asal dan tujuan tidak boleh sama.")
            else:
                st.info("Daftarkan minimal 2 kota terlebih dahulu.")
                
    # 2. Action: Update
    with tab2:
        st.write("##")
        daftar_kota = list(graph.keys())
        if daftar_kota:
            asal_up = st.selectbox("Kota Asal", daftar_kota, key="u_asal")
            rute_ada = list(graph.get(asal_up, {}).keys())
            
            if rute_ada:
                tujuan_up = st.selectbox("Kota Tujuan", rute_ada, key="u_tuj")
                jarak_baru = st.number_input("Perbarui Jarak Baru (km)", min_value=1, value=int(graph[asal_up][tujuan_up]))
                if st.button("Simpan Perubahan Jalur", use_container_width=True):
                    graph[asal_up][tujuan_up] = jarak_baru
                    graph[tujuan_up][asal_up] = jarak_baru
                    st.success("Sukses: Data jarak logistik diperbarui.")
                    st.rerun()
            else:
                st.info(f"Kota {asal_up} belum memiliki rute distribusi.")
        else:
            st.info("Belum ada data kota.")

    # 3. Action: Delete
    with tab3:
        st.write("##")
        daftar_kota = list(graph.keys())
        if daftar_kota:
            kota_del = st.selectbox("Pilih Kota Yang Akan Dihapus", daftar_kota, key="d_kota")
            st.markdown("<p style='color: #dc3545; font-size: 14px;'>⚠️ Menghapus kota ini akan otomatis membatalkan semua rute pengiriman yang terhubung dengannya!</p>", unsafe_allow_html=True)
            if st.button("Hapus Kota & Rute Terkait", type="primary", use_container_width=True):
                for tetangga in list(graph[kota_del].keys()):
                    del graph[tetangga][kota_del]
                del graph[kota_del]
                st.success(f"Kota {kota_del} dibersihkan dari sistem.")
                st.rerun()
        else:
            st.info("Tidak ada data kota.")
            
    st.markdown('</div>', unsafe_allow_html=True) # Tutup Card Kontrol

# ------------------------------------------
# KOLOM KANAN: PANEL MONITORING (DATA READ)
# ------------------------------------------
with kolom_monitor:
    st.markdown("<h3 style='color: #1e3d59;'>📊 Monitor Jaringan Distribusi</h3>", unsafe_allow_html=True)
    
    # Hitung jumlah total node dan total edge untuk counter aplikasi
    total_kota = len(graph.keys())
    total_rute = sum([len(tujuan) for tujuan in graph.values()]) // 2
    
    # Menampilkan Metric/Counter Ringkas ala Dashboard Aplikasi
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(label="Total Titik Distribusi (Nodes)", value=f"{total_kota} Kota")
    with col_m2:
        st.metric(label="Total Jalur Aktif (Edges)", value=f"{total_rute} Rute")
        
    st.write("##")
    
    # Bungkus tabel data di dalam komponen Card
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("<p style='font-weight: bold; color: #1e3d59; margin-top:0;'>📋 Manifes Data Rute (Live Data)</p>", unsafe_allow_html=True)
    
    # Olah data graph dict menjadi DataFrame Pandas agar berbentuk tabel tabular terstruktur
    data_tabel = []
    for kota_asal, tujuan_dict in graph.items():
        if tujuan_dict:
            for kota_tujuan, jarak in tujuan_dict.items():
                data_tabel.append({"Asal": kota_asal, "Tujuan": kota_tujuan, "Jarak Operasional": f"{jarak} km"})
        else:
            data_tabel.append({"Asal": kota_asal, "Tujuan": "Belum Terhubung", "Jarak Operasional": "-"})

    if data_tabel:
        df = pd.DataFrame(data_tabel)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Sistem kosong. Belum ada manifes rute terdaftar.")
        
    st.markdown('</div>',

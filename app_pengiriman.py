import streamlit as st
import pandas as pd

# ==========================================
# 🎨 KUSTOMISASI STYLE & BACKGROUND (CSS)
# ==========================================
def set_background():
    st.markdown(
        """
        <style>
        /* Mengubah background utama aplikasi */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Mengubah styling card/container tabel agar lebih kontras */
        .stDataFrame {
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        /* Mengubah styling teks judul utama */
        h1 {
            color: #1e3d59;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-weight: 800;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Panggil fungsi background di awal halaman
set_background()

# ==========================================
# 📦 INISIALISASI STATE (Data Awal)
# ==========================================
if 'graph' not in st.session_state:
    st.session_state.graph = {
        "Jakarta": {"Bandung": 150, "Semarang": 450},
        "Bandung": {"Jakarta": 150, "Semarang": 370},
        "Semarang": {"Jakarta": 450, "Bandung": 370, "Surabaya": 350},
        "Surabaya": {"Semarang": 350}
    }

graph = st.session_state.graph

# Header Utama
st.title("📦 Dashboard Rute Pengiriman Logistik")
st.caption("Aplikasi Graph Logistik Terintegrasi CRUD")

# ==========================================
# 📊 TABEL RINGKASAN DATA (READ)
# ==========================================
st.subheader("🗺️ Tabel Rute Saat Ini")
data_tabel = []
for kota_asal, tujuan_dict in graph.items():
    if tujuan_dict:
        for kota_tujuan, jarak in tujuan_dict.items():
            data_tabel.append({"Kota Asal": kota_asal, "Kota Tujuan": kota_tujuan, "Jarak (km)": jarak})
    else:
        data_tabel.append({"Kota Asal": kota_asal, "Kota Tujuan": "-", "Jarak (km)": 0})

if data_tabel:
    st.dataframe(pd.DataFrame(data_tabel), use_container_width=True)
else:
    st.info("Belum ada data pengiriman.")

# ==========================================
# 🗂️ MENU CRUD (TABS)
# ==========================================
tab1, tab2, tab3 = st.tabs(["➕ Create (Tambah)", "🔄 Update (Ubah)", "❌ Delete (Hapus)"])

# 1. TAB CREATE
with tab1:
    st.subheader("Tambah Kota atau Rute Baru")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📍 Tambah Node (Kota)**")
        kota_baru = st.text_input("Nama Kota Baru", placeholder="Contoh: Yogyakarta").strip()
        if st.button("Simpan Kota"):
            if kota_baru and kota_baru not in graph:
                graph[kota_baru] = {}
                st.success(f"Kota {kota_baru} berhasil ditambahkan!")
                st.rerun()
            elif kota_baru in graph:
                st.warning("Kota sudah terdaftar.")
                
    with col2:
        st.markdown("**🛣️ Tambah Edge (Rute)**")
        daftar_kota = list(graph.keys())
        if len(daftar_kota) >= 2:
            asal = st.selectbox("Kota Asal", daftar_kota, key="c_asal")
            tujuan = st.selectbox("Kota Tujuan", daftar_kota, key="c_tuj")
            jarak = st.number_input("Jarak (km)", min_value=1, value=100)
            if st.button("Hubungkan Rute"):
                if asal != tujuan:
                    graph[asal][tujuan] = jarak
                    graph[tujuan][asal] = jarak
                    st.success(f"Rute {asal} - {tujuan} ditambahkan!")
                    st.rerun()
                else:
                    st.error("Kota asal dan tujuan tidak boleh sama.")

# 2. TAB UPDATE
with tab2:
    st.subheader("Ubah Jarak Antar Kota")
    daftar_kota = list(graph.keys())
    asal_up = st.selectbox("Pilih Kota Asal", daftar_kota, key="u_asal")
    rute_ada = list(graph.get(asal_up, {}).keys())
    
    if rute_ada:
        tujuan_up = st.selectbox("Pilih Kota Tujuan", rute_ada, key="u_tuj")
        jarak_baru = st.number_input("Jarak Baru (km)", min_value=1, value=int(graph[asal_up][tujuan_up]))
        if st.button("Perbarui Jarak"):
            graph[asal_up][tujuan_up] = jarak_baru
            graph[tujuan_up][asal_up] = jarak_baru
            st.success("Jarak rute berhasil diperbarui!")
            st.rerun()
    else:
        st.info(f"Kota {asal_up} belum memiliki rute keluar.")

# 3. TAB DELETE
with tab3:
    st.subheader("Hapus Node / Kota")
    daftar_kota = list(graph.keys())
    if daftar_kota:
        kota_del = st.selectbox("Pilih Kota yang Ingin Dihapus", daftar_kota, key="d_kota")
        st.warning(f"Menghapus {kota_del} juga akan menghapus rute yang terhubung dengannya.")
        if st.button("Hapus Kota Permanen", type="primary"):
            for tetangga in list(graph[kota_del].keys()):
                del graph[tetangga][kota_del]
            del graph[kota_del]
            st.success(f"Kota {kota_del} berhasil dihapus.")
            st.rerun()
    else:
        st.info("Tidak ada kota tersisa.")

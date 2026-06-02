import streamlit as st
import pandas as pd

# ==========================================
# INISIALISASI STATE (Data Awal)
# ==========================================
if 'graph' not in st.session_state:
    st.session_state.graph = {
        "Jakarta": {"Bandung": 150, "Semarang": 450},
        "Bandung": {"Jakarta": 150, "Semarang": 370},
        "Semarang": {"Jakarta": 450, "Bandung": 370, "Surabaya": 350},
        "Surabaya": {"Semarang": 350}
    }

graph = st.session_state.graph

st.title("📦 CRUD Rute Pengiriman (Tanpa Matplotlib)")

# ==========================================
# TABEL RINGKASAN DATA (READ)
# ==========================================
st.subheader("📊 Tabel Rute Saat Ini")
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
    st.info("Belum ada data.")

# ==========================================
# MENU CRUD (TABS)
# ==========================================
tab1, tab2, tab3 = st.tabs(["➕ Create", "🔄 Update", "❌ Delete"])

with tab1:
    st.subheader("Tambah Kota atau Rute")
    col1, col2 = st.columns(2)
    
    with col1:
        kota_baru = st.text_input("Nama Kota Baru").strip()
        if st.button("Tambah Kota"):
            if kota_baru and kota_baru not in graph:
                graph[kota_baru] = {}
                st.success(f"{kota_baru} ditambahkan!")
                st.rerun()
                
    with col2:
        daftar_kota = list(graph.keys())
        if len(daftar_kota) >= 2:
            asal = st.selectbox("Asal", daftar_kota, key="c_asal")
            tujuan = st.selectbox("Tujuan", daftar_kota, key="c_tuj")
            jarak = st.number_input("Jarak (km)", min_value=1, value=100)
            if st.button("Tambah Rute"):
                if asal != tujuan:
                    graph[asal][tujuan] = jarak
                    graph[tujuan][asal] = jarak
                    st.success("Rute ditambahkan!")
                    st.rerun()

with tab2:
    st.subheader("Ubah Jarak Rute")
    daftar_kota = list(graph.keys())
    asal_up = st.selectbox("Pilih Kota Asal", daftar_kota, key="u_asal")
    rute_ada = list(graph.get(asal_up, {}).keys())
    
    if rute_ada:
        tujuan_up = st.selectbox("Pilih Kota Tujuan", rute_ada, key="u_tuj")
        jarak_baru = st.number_input("Jarak Baru", min_value=1, value=int(graph[asal_up][tujuan_up]))
        if st.button("Update Jarak"):
            graph[asal_up][tujuan_up] = jarak_baru
            graph[tujuan_up][asal_up] = jarak_baru
            st.success("Jarak diperbarui!")
            st.rerun()

with tab3:
    st.subheader("Hapus Data")
    daftar_kota = list(graph.keys())
    kota_del = st.selectbox("Hapus Kota Total", daftar_kota, key="d_kota")
    if st.button("Hapus Kota", type="primary"):
        for tetangga in list(graph[kota_del].keys()):
            del graph[tetangga][kota_del]
        del graph[kota_del]
        st.success(f"{kota_del} dihapus!")
        st.rerun()
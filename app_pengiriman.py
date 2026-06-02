import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

# Konfigurasi halaman agar melebar penuh (Wide Mode)
st.set_page_config(layout="wide", page_title="Logistics Graph App")

# ==========================================
# 🎨 CSS KUSTOM: BACKGROUND GRID
# ==========================================
def set_app_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f8fafc;
            background-image: radial-gradient(#e2e8f0 1.5px, transparent 1.5px);
            background-size: 24px 24px;
        }
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
        div.custom-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            border: 1px solid #e2e8f0;
        }
        .stTabs [aria-selected="true"] {
            background-color: #0f172a !important;
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
        "Surabaya": {"Semarang": 350},
        "Yogyakarta": {"Bandung": 400, "Semarang": 120}
    }

graph = st.session_state.graph

# ==========================================
# 📐 LAYOUT UTAMA APLIKASI
# ==========================================

st.markdown("<h1 style='color: #0f172a; margin-bottom: 0; font-weight: 800;'>🚀 LOGIX - Rute Graph Navigator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; margin-top: 0; margin-bottom: 30px; font-size: 16px;'>Sistem Manajemen Node & Jalur Distribusi Logistik Perusahaan</p>", unsafe_allow_html=True)

# Membagi layar menjadi 2 kolom: Kiri (Form CRUD & Tabel) & Kanan (Peta Graph Interaktif)
kolom_kiri, kolom_kanan = st.columns([1.1, 1.3], gap="large")

# ------------------------------------------
# KOLOM KIRI: MANAGEMENT & MANIFES DATA
# ------------------------------------------
with kolom_kiri:
    st.markdown("<h3 style='color: #0f172a; font-size: 20px;'>⚙️ Panel Manajemen & CRUD</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["➕ TAMBAH DATA", "🔄 UPDATE JARAK", "❌ HAPUS DATA"])
    
    # 1. Action: Create
    with tab1:
        st.write("##")
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
    
    # 2. Action: Update
    with tab2:
        st.write("##")
        daftar_kota = list(graph.keys())
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
            st.info("Kota ini belum memiliki rute pengiriman.")

    # 3. Action: Delete
    with tab3:
        st.write("##")
        daftar_kota = list(graph.keys())
        kota_del = st.selectbox("Pilih Kota Yang Akan Dihapus", daftar_kota, key="d_kota")
        if st.button("Hapus Kota & Rute Terkait", type="primary", use_container_width=True):
            for tetangga in list(graph[kota_del].keys()):
                del graph[tetangga][kota_del]
            del graph[kota_del]
            st.success(f"Kota {kota_del} dibersihkan.")
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Manifes Live Data (Tabel)
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("<p style='font-weight: bold; color: #0f172a; margin-top:0;'>📋 Manifes Data Rute (Tabel)</p>", unsafe_allow_html=True)
    data_tabel = []
    for kota_asal, tujuan_dict in graph.items():
        for kota_tujuan, jarak in tujuan_dict.items():
            data_tabel.append({"Asal": kota_asal, "Tujuan": kota_tujuan, "Jarak": f"{jarak} km"})
    if data_tabel:
        st.dataframe(pd.DataFrame(data_tabel), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# KOLOM KANAN: LIVE INTERACTIVE GRAPH RADAR
# ------------------------------------------
with kolom_kanan:
    st.markdown("<h3 style='color: #0f172a; font-size: 20px;'>🗺️ Peta Graph Interaktif (Real-time Radar)</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    # --- PROSES IDENTIFIKASI RUTE TERCEPAT / HUB TERBANYAK ---
    # Cari kota mana yang punya rute paling banyak (Hub Utama)
    hub_terbanyak = ""
    maks_rute = 0
    for kota, rute in graph.items():
        if len(rute) > maks_rute:
            maks_rute = len(rute)
            hub_terbanyak = kota

    # Cari rute dengan jarak paling pendek / tercepat secara keseluruhan
    rute_tercepat_asal = ""
    rute_tercepat_tujuan = ""
    jarak_terpendek = float('inf')
    
    for kota_asal, tujuan_dict in graph.items():
        for kota_tujuan, jarak in tujuan_dict.items():
            if jarak < jarak_terpendek:
                jarak_terpendek = jarak
                rute_tercepat_asal = kota_asal
                rute_tercepat_tujuan = kota_tujuan

    # --- MEMBANGUN GRAFIK AGRAPH ---
    nodes = []
    edges = []
    
    # 1. Daftarkan Semua Node (Kota)
    for kota in graph.keys():
        # Jika kota tersebut adalah Hub Terbanyak, beri warna emas/kuning, jika tidak beri warna biru
        if kota == hub_terbanyak:
            nodes.append(Node(id=kota, label=f"⭐ {kota} (Hub)", size=25, color="#f59e0b"))
        else:
            nodes.append(Node(id=kota, label=kota, size=20, color="#3b82f6"))
            
    # 2. Daftarkan Semua Edge (Garis Jalur)
    rute_tercatat = set()
    for kota_asal, tujuan_dict in graph.items():
        for kota_tujuan, jarak in tujuan_dict.items():
            # Agar rute bolak-balik tidak digambar dua kali
            rute_id = tuple(sorted([kota_asal, kota_tujuan]))
            if rute_id not in rute_tercatat:
                rute_tercatat.add(rute_id)
                
                # Highlight warna MERAH jika rute tersebut merupakan rute paling pendek/tercepat
                if (kota_asal == rute_tercepat_asal and kota_tujuan == rute_tercepat_tujuan) or \
                   (kota_asal == rute_tercepat_tujuan and kota_tujuan == rute_tercepat_asal):
                    edges.append(Edge(source=kota_asal, target=kota_tujuan, label=f"🚀 TERCEPAT ({jarak}km)", color="#ef4444", strokeWidth=4))
                else:
                    edges.append(Edge(source=kota_asal, target=kota_tujuan, label=f"{jarak} km", color="#94a3b8", strokeWidth=2))

    # 3. Konfigurasi Tampilan Graph
    config = Config(
        width=650,
        height=500,
        directed=False, # Dua arah (Undirected Graph)
        physics=True,   # Membuat efek membal/elastis saat digeser
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#10b981"
    )
    
    # Render Graph ke halaman web
    agraph(nodes=nodes, edges=edges, config=config)
    
    # Keterangan Legenda Menu
    st.markdown("""
    **💡 Informasi Radar:**
    * 🟡 **Kota dengan Simbol ⭐ (Kuning)**: Adalah Hub Logistik utama (memiliki rute terbanyak).
    * 🔴 **Garis Merah Tebal**: Menandakan rute operasional langsung **paling pendek / tercepat** saat ini di sistem.
    * *Tips: Anda bisa mengklik dan menggeser kota di atas secara langsung dengan mouse Anda!*
    """)
    st.markdown('</div>', unsafe_allow_html=True)

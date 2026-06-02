import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# Konfigurasi Halaman Mode Lebar & Judul Aplikasi
st.set_page_config(layout="wide", page_title="LOGIX - Navigator Rute Jaringan", page_icon="🚀")

# ==========================================
# 🎨 KUSTOMISASI CSS: ULTRA DARK & WHITE TEXT MODE
# ==========================================
def set_dark_app_theme():
    st.markdown(
        """
        <style>
        /* Mengubah total warna background utama aplikasi */
        .stApp {
            background-color: #0f172a;
            background-image: radial-gradient(#1e293b 2px, transparent 2px);
            background-size: 30px 30px;
        }
        
        /* Font Global & Warna Teks Utama Jadi Putih */
        html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            color: #ffffff !important;
        }
        
        /* Memaksa label input dan judul komponen menjadi putih */
        label, .stRadio legend, div[data-testid="stWidgetLabel"] p {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Desain Kotak Kartu Aplikasi (Dark Glass Card) */
        div.custom-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #334155;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
            margin-bottom: 24px;
        }
        
        /* Mengubah styling TAB agar menyatu dengan Tema Aplikasi */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: 2px solid #334155;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #1e293b;
            border-radius: 8px 8px 0px 0px;
            padding: 10px 20px;
            font-weight: bold;
            color: #cbd5e1 !important; /* Warna tab tidak aktif dibuat abu terang agar terbaca */
            border: 1px solid #334155;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2563eb !important;
            color: #ffffff !important;
            border-bottom: none !important;
        }
        
        /* Mempercantik Input Teks & Select Box */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
        }
        
        /* Tombol Utama (Confirm Button) */
        .stButton button {
            background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: bold !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
            transition: all 0.2s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_dark_app_theme()

# ==========================================
# 📦 STATE MANAGEMENT (Data Graph)
# ==========================================
if 'graph' not in st.session_state:
    st.session_state.graph = {
        "Jakarta": {"Bandung": 150, "Semarang": 450, "Surabaya": 780},
        "Bandung": {"Jakarta": 150, "Yogyakarta": 400},
        "Semarang": {"Jakarta": 450, "Yogyakarta": 120, "Surabaya": 350},
        "Surabaya": {"Jakarta": 780, "Semarang": 350},
        "Yogyakarta": {"Bandung": 400, "Semarang": 120}
    }

graph = st.session_state.graph

# ==========================================
# 📊 LOGIKA OPERASIONAL GRAPH
# ==========================================
hub_terbanyak = ""
maks_rute = 0
for kota, rute in graph.items():
    if len(rute) > maks_rute:
        maks_rute = len(rute)
        hub_terbanyak = kota

rute_tercepat_asal, rute_tercepat_tujuan = "", ""
jarak_terpendek = float('inf')
for kota_asal, tujuan_dict in graph.items():
    for kota_tujuan, jarak in tujuan_dict.items():
        if jarak < jarak_terpendek:
            jarak_terpendek = jarak
            rute_tercepat_asal = kota_asal
            rute_tercepat_tujuan = kota_tujuan

total_kota = len(graph.keys())
total_rute = sum([len(tujuan) for tujuan in graph.values()]) // 2

# ==========================================
# 📐 LAYOUT UTAMA DASHBOARD
# ==========================================

st.markdown("<h1 style='text-align: center; color: #ffffff; font-weight: 800; font-size: 36px; margin-bottom:0;'>🚀 LOGIX - Navigator Rute Jaringan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px; margin-top:5px; margin-bottom:40px;'>Sistem Manajemen Node dan Rute Distribusi Logistik Perusahaan</p>", unsafe_allow_html=True)

kolom_kiri, kolom_kanan = st.columns([1, 1.4], gap="large")

# ------------------------------------------
# ⚙️ KOLOM KIRI: PANEL MANAJEMEN DATA (CRUD)
# ------------------------------------------
with kolom_kiri:
    st.markdown("<h4 style='color: #ffffff; margin-bottom: 12px; font-weight:700;'>⚙️ Panel Kontrol Operasional</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["➕ TAMBAH DATA", "🔄 UPDATE JARAK", "❌ HAPUS DATA"])
    
    # Tab 1: Create
    with tab1:
        st.write("##")
        pilihan_input = st.radio("Pilih Jenis Komponen:", ["Titik Kota Baru (Node)", "Jalur Antar Kota (Edge)"], horizontal=True)
        st.write("---")
        
        if pilihan_input == "Titik Kota Baru (Node)":
            kota_baru = st.text_input("Nama Kota Baru", placeholder="Contoh: Malang").strip()
            if st.button("Konfirmasi Pendaftaran Kota", use_container_width=True):
                if kota_baru and kota_baru not in graph:
                    graph[kota_baru] = {}
                    st.success(f"Sukses: Kota '{kota_baru}' berhasil terdaftar!")
                    st.rerun()
                elif kota_baru in graph:
                    st.warning("Peringatan: Nama kota tersebut sudah ada di sistem.")
        else:
            daftar_kota = list(graph.keys())
            if len(daftar_kota) >= 2:
                asal = st.selectbox("Kota Asal", daftar_kota, key="c_asal")
                tujuan = st.selectbox("Kota Tujuan", daftar_kota, key="c_tuj")
                jarak = st.number_input("Jarak Operasional (km)", min_value=1, value=100)
                if st.button("Hubungkan Rute Baru", use_container_width=True):
                    if asal != tujuan:
                        graph[asal][tujuan] = jarak
                        graph[tujuan][asal] = jarak
                        st.success("Sukses: Jalur distribusi baru berhasil diaktifkan!")
                        st.rerun()
                    else:
                        st.error("Gagal: Kota asal dan kota tujuan tidak boleh sama.")
    
    # Tab 2: Update
    with tab2:
        st.write("##")
        daftar_kota = list(graph.keys())
        if daftar_kota:
            asal_up = st.selectbox("Kota Asal", daftar_kota, key="u_asal")
            rute_ada = list(graph.get(asal_up, {}).keys())
            if rute_ada:
                tujuan_up = st.selectbox("Kota Tujuan", rute_ada, key="u_tuj")
                jarak_baru = st.number_input("Sesuaikan Jarak Baru (km)", min_value=1, value=int(graph[asal_up][tujuan_up]))
                if st.button("Simpan Perubahan Perbarui", use_container_width=True):
                    graph[asal_up][tujuan_up] = jarak_baru
                    graph[tujuan_up][asal_up] = jarak_baru
                    st.success("Sukses: Data jarak operasional berhasil diubah!")
                    st.rerun()
            else:
                st.info("Info: Kota ini belum memiliki rute keluar aktif.")
        else:
            st.info("Belum ada data kota di dalam sistem.")

    # Tab 3: Delete
    with tab3:
        st.write("##")
        daftar_kota = list(graph.keys())
        if daftar_kota:
            kota_del = st.selectbox("Pilih Kota yang Ingin Dihapus", daftar_kota, key="d_kota")
            st.markdown("<p style='color: #f43f5e; font-size: 14px; font-weight: bold;'>⚠️ Perhatian: Menghapus kota ini otomatis memutus semua rute pengiriman yang terhubung dengannya!</p>", unsafe_allow_html=True)
            if st.button("Hapus Kota Total dari Jaringan", type="primary", use_container_width=True):
                for tetangga in list(graph[kota_del].keys()):
                    del graph[tetangga][kota_del]
                del graph[kota_del]
                st.success("Sukses: Data kota dan jalurnya berhasil dibersihkan.")
                st.rerun()
        else:
            st.info("Tidak ada data kota untuk dihapus.")
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Panel Manifes Ringkasan Data Live
    st.markdown("<h4 style='color: #ffffff; margin-bottom: 12px; font-weight:700;'>📋 Manifes Data Distribusi (Live)</h4>", unsafe_allow_html=True)
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    with col_inf1:
        st.markdown(f'<div class="custom-card" style="text-align:center; padding:15px;"><span style="color:#94a3b8; font-size:12px; font-weight:600;">TOTAL KOTA</span><br><strong style="font-size:24px; color:#38bdf8;">{total_kota}</strong></div>', unsafe_allow_html=True)
    with col_inf2:
        st.markdown(f'<div class="custom-card" style="text-align:center; padding:15px;"><span style="color:#94a3b8; font-size:12px; font-weight:600;">TOTAL JALUR</span><br><strong style="font-size:24px; color:#34d399;">{total_rute}</strong></div>', unsafe_allow_html=True)
    with col_inf3:
        st.markdown(f'<div class="custom-card" style="text-align:center; padding:15px;"><span style="color:#94a3b8; font-size:12px; font-weight:600;">HUB UTAMA</span><br><strong style="font-size:15px; color:#fbbf24;">{hub_terbanyak if hub_terbanyak else "-"}</strong></div>', unsafe_allow_html=True)

# ------------------------------------------
# 🗺️ KOLOM KANAN: RADAR MAPS INTERAKTIF REAL-TIME
# ------------------------------------------
with kolom_kanan:
    st.markdown("<h4 style='color: #ffffff; margin-bottom: 12px; font-weight:700;'>🗺️ Peta Jaringan Interaktif (Radar Real-Time)</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card" style="background-color: #0b1329;">', unsafe_allow_html=True)
    
    col_ind1, col_ind2, col_ind3 = st.columns(3)
    with col_ind1:
        st.markdown(f'<p style="color:#94a3b8; font-size:11px; margin-bottom:2px; font-weight:600;">TOTAL KOTA (NODES)</p><h5 style="color:#ffffff; margin-top:0; font-weight:700;">👥 {total_kota} Kota</h5>', unsafe_allow_html=True)
    with col_ind2:
        st.markdown(f'<p style="color:#94a3b8; font-size:11px; margin-bottom:2px; font-weight:600;">TOTAL RUTE (EDGES)</p><h5 style="color:#ffffff; margin-top:0; font-weight:700;">🔀 {total_rute} Jalur</h5>', unsafe_allow_html=True)
    with col_ind3:
        if rute_tercepat_asal:
            st.markdown(f'<p style="color:#f43f5e; font-size:11px; margin-bottom:2px; font-weight:bold;">🚀 RUTE TERCEPAT SAAT INI</p><h5 style="color:#ffffff; margin-top:0; font-weight:700;">{rute_tercepat_asal} ↔️ {rute_tercepat_tujuan} ({jarak_terpendek} km)</h5>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#94a3b8; font-size:11px; margin-bottom:2px; font-weight:600;">🚀 RUTE TERCEPAT SAAT INI</p><h5 style="color:#ffffff; margin-top:0; font-weight:700;">-</h5>', unsafe_allow_html=True)
            
    st.write("---")
    
    # Menyiapkan data Node & Edge JSON untuk JavaScript Vis.js (Tema Glow-Dark)
    vis_nodes = []
    vis_edges = []
    
    for kota in graph.keys():
        if kota == hub_terbanyak and len(graph[kota]) > 0:
            vis_nodes.append({"id": kota, "label": f"⭐ {kota}\n(HUB UTAMA)", "color": {"background": "#f59e0b", "border": "#d97706"}, "font": {"color": "#ffffff", "size": 13, "bold": True}, "size": 25})
        else:
            vis_nodes.append({"id": kota, "label": kota, "color": {"background": "#38bdf8", "border": "#0284c7"}, "font": {"color": "#cbd5e1", "size": 12}, "size": 16})
            
    rute_tercatat = set()
    for kota_asal, tujuan_dict in graph.items():
        for kota_tujuan, jarak in tujuan_dict.items():
            rute_id = tuple(sorted([kota_asal, kota_tujuan]))
            if rute_id not in rute_tercatat:
                rute_tercatat.add(rute_id)
                
                is_tercepat = (kota_asal == rute_tercepat_asal and kota_tujuan == rute_tercepat_tujuan) or \
                             (kota_asal == rute_tercepat_tujuan and kota_tujuan == rute_tercepat_asal)
                
                if is_tercepat:
                    vis_edges.append({"from": kota_asal, "to": kota_tujuan, "label": f"🚀 {jarak} km", "color": {"color": "#f43f5e", "highlight": "#f43f5e"}, "width": 4.5, "font": {"color": "#f43f5e", "strokeWidth": 0}})
                else:
                    vis_edges.append({"from": kota_asal, "to": kota_tujuan, "label": f"{jarak} km", "color": {"color": "#475569", "highlight": "#64748b"}, "width": 1.5, "font": {"color": "#94a3b8", "strokeWidth": 0}})

    # Memasukkan Script HTML Vis.js dengan konfigurasi Dark-Blue Glow
    html_code = f"""
    <div id="mynetwork" style="width: 100%; height: 460px; background-color: #0b1329; border: 1px solid #1e293b; border-radius: 12px;"></div>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(vis_nodes)});
        var edges = new vis.DataSet({json.dumps(vis_edges)});
        var container = document.getElementById('mynetwork');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
            nodes: {{ shape: 'dot', font: {{ face: 'Inter' }} }},
            edges: {{ font: {{ align: 'top' }} }},
            physics: {{ stabilization: true, barnesHut: {{ gravitationalConstant: -1500, centralGravity: 0.4, springLength: 130 }} }}
        }};
        var network = new vis.Network(container, data, options);
    </script>
    """
    
    components.html(html_code, height=480)
    st.markdown("<p style='color: #94a3b8; font-size: 12px; text-align: center; margin-top:10px;'>
    
                ⚡ RUTE TERCEPAT di-highlight otomatis dengan jalur warna merah menyala secara real-time.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

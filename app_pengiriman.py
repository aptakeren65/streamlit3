import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# Konfigurasi halaman agar melebar penuh (Wide Mode)
st.set_page_config(layout="wide", page_title="LOGIX - Graph Dashboard", page_icon="🚀")

# ==========================================
# 🎨 CSS KUSTOM: DESAIN PREMIUM UTAMA
# ==========================================
def set_app_theme():
    st.markdown(
        """
        <style>
        /* Latar Belakang Aplikasi dengan Pola Grid */
        .stApp {
            background-color: #f8fafc;
            background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px);
            background-size: 24px 24px;
        }
        
        /* Font Global */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
        
        /* Desain Kartu (Card Layout) */
        div.custom-card {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
            margin-bottom: 24px;
            border: 1px solid #e2e8f0;
        }
        
        /* Kartu Khusus Informasi Jalur Tercepat */
        div.fastest-card {
            background: linear-gradient(135deg, #fef2f2 0%, #ffe4e6 100%);
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #fecdd3;
            margin-bottom: 15px;
        }
        
        /* Modifikasi Tampilan Tab CRUD */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: 2px solid #e2e8f0;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f1f5f9;
            border-radius: 8px 8px 0px 0px;
            padding: 12px 24px;
            font-weight: 700;
            color: #475569;
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
# 📊 ALGORITMA & PERHITUNGAN DATA GRAPH
# ==========================================
# 1. Cari Hub Utama (Koneksi terbanyak)
hub_terbanyak = ""
maks_rute = 0
for kota, rute in graph.items():
    if len(rute) > maks_rute:
        maks_rute = len(rute)
        hub_terbanyak = kota

# 2. Cari Jalur Langsung Tercepat (Jarak minimum)
rute_tercepat_asal = ""
rute_tercepat_tujuan = ""
jarak_terpendek = float('inf')
for kota_asal, tujuan_dict in graph.items():
    for kota_tujuan, jarak in tujuan_dict.items():
        if jarak < jarak_terpendek:
            jarak_terpendek = jarak
            rute_tercepat_asal = kota_asal
            rute_tercepat_tujuan = kota_tujuan

# ==========================================
# 📐 LAYOUT UTAMA DASHBOARD
# ==========================================

# Top Bar / Header Utama
st.markdown("<h1 style='color: #0f172a; margin-bottom: 0; font-weight: 800; font-size: 32px;'>🚀 LOGIX - Dashboard Logistik</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; margin-top: 5px; margin-bottom: 30px; font-size: 16px;'>Manajemen Graph Jaringan Distribusi dan Rute Pengiriman Real-Time</p>", unsafe_allow_html=True)

# Pembagian Dua Kolom Utama (Kiri: Manajemen & Manifes | Kanan: Visualisasi & Metrik)
kolom_kiri, kolom_kanan = st.columns([1.1, 1.3], gap="large")

# ------------------------------------------
# ⚙️ KOLOM KIRI: PANEL OPERASIONAL (CRUD)
# ------------------------------------------
with kolom_kiri:
    st.markdown("<h3 style='color: #0f172a; font-size: 20px; font-weight: 700; margin-bottom:15px;'>⚙️ Kontrol Data Jaringan</h3>", unsafe_allow_html=True)
    
    # Boks Kartu Form CRUD
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["➕ TAMBAH DATA", "🔄 UPDATE JARAK", "❌ HAPUS DATA"])
    
    # 1. CREATE ACTION
    with tab1:
        st.write("##")
        pilihan_input = st.radio("Pilih Jenis Data Baru:", ["Titik Kota (Node)", "Jalur Rute (Edge)"], horizontal=True)
        st.write("---")
        
        if pilihan_input == "Titik Kota (Node)":
            kota_baru = st.text_input("Nama Kota Baru", placeholder="Contoh: Malang").strip()
            if st.button("Daftarkan Kota Baru", use_container_width=True):
                if kota_baru and kota_baru not in graph:
                    graph[kota_baru] = {}
                    st.success(f"Berhasil: Kota '{kota_baru}' kini aktif di jaringan.")
                    st.rerun()
                elif kota_baru in graph:
                    st.warning("Peringatan: Kota tersebut sudah terdaftar.")
        else:
            daftar_kota = list(graph.keys())
            if len(daftar_kota) >= 2:
                asal = st.selectbox("Kota Asal", daftar_kota, key="c_asal")
                tujuan = st.selectbox("Kota Tujuan", daftar_kota, key="c_tuj")
                jarak = st.number_input("Jarak Operasional (km)", min_value=1, value=100)
                if st.button("Hubungkan Rute Distribusi", use_container_width=True):
                    if asal != tujuan:
                        graph[asal][tujuan] = jarak
                        graph[tujuan][asal] = jarak
                        st.success(f"Berhasil: Jalur {asal} ↔️ {tujuan} aktif.")
                        st.rerun()
                    else:
                        st.error("Kesalahan: Kota asal dan tujuan tidak boleh sama.")
            else:
                st.info("Info: Harap daftarkan minimal 2 kota terlebih dahulu.")
    
    # 2. UPDATE ACTION
    with tab2:
        st.write("##")
        daftar_kota = list(graph.keys())
        if daftar_kota:
            asal_up = st.selectbox("Pilih Kota Asal", daftar_kota, key="u_asal")
            rute_ada = list(graph.get(asal_up, {}).keys())
            if rute_ada:
                tujuan_up = st.selectbox("Pilih Kota Tujuan", rute_ada, key="u_tuj")
                jarak_baru = st.number_input("Sesuaikan Jarak Baru (km)", min_value=1, value=int(graph[asal_up][tujuan_up]))
                if st.button("Perbarui Data Jarak", use_container_width=True):
                    graph[asal_up][tujuan_up] = jarak_baru
                    graph[tujuan_up][asal_up] = jarak_baru
                    st.success("Berhasil: Jarak operasional diperbarui.")
                    st.rerun()
            else:
                st.info(f"Kota {asal_up} belum memiliki jalur keluar.")
        else:
            st.info("Belum ada data kota.")

    # 3. DELETE ACTION
    with tab3:
        st.write("##")
        daftar_kota = list(graph.keys())
        if daftar_kota:
            kota_del = st.selectbox("Pilih Kota yang Ingin Dihapus", daftar_kota, key="d_kota")
            st.markdown("<p style='color: #ef4444; font-size: 14px; font-weight: 500;'>⚠️ Perhatian: Menghapus kota ini akan otomatis menghapus seluruh rute pengiriman yang terhubung dengannya!</p>", unsafe_allow_html=True)
            if st.button("Hapus Kota dari Jaringan", type="primary", use_container_width=True):
                for tetangga in list(graph[kota_del].keys()):
                    del graph[tetangga][kota_del]
                del graph[kota_del]
                st.success(f"Sukses: Kota {kota_del} telah dihapus.")
                st.rerun()
        else:
            st.info("Tidak ada data kota untuk dihapus.")
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Manifes Live Data (Tabel)
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("<p style='font-weight: 700; color: #0f172a; margin-top:0; font-size:16px;'>📋 Manifes Data Tabel</p>", unsafe_allow_html=True)
    data_tabel = []
    for kota_asal, tujuan_dict in graph.items():
        for kota_tujuan, jarak in tujuan_dict.items():
            data_tabel.append({"Kota Asal": kota_asal, "Kota Tujuan": kota_tujuan, "Jarak": f"{jarak} km"})
    if data_tabel:
        st.dataframe(pd.DataFrame(data_tabel), use_container_width=True, hide_index=True)
    else:
        st.caption("Jaringan kosong.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# 🗺️ KOLOM KANAN: MONITOR LIVE & METRIK GRAPH
# ------------------------------------------
with kolom_kanan:
    st.markdown("<h3 style='color: #0f172a; font-size: 20px; font-weight: 700; margin-bottom:15px;'>🗺️ Peta Radar & Metrik Jaringan</h3>", unsafe_allow_html=True)
    
    # 1. Baris Metrik Ringkasan di Bagian Atas
    total_kota = len(graph.keys())
    total_rute = sum([len(tujuan) for tujuan in graph.values()]) // 2
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f'<div class="custom-card"><span style="color:#64748b; font-size:14px; font-weight:500;">Total Node Jaringan</span><br><strong style="font-size:28px; color:#0f172a;">{total_kota} Kota</strong></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div class="custom-card"><span style="color:#64748b; font-size:14px; font-weight:500;">Total Rute Aktif</span><br><strong style="font-size:28px; color:#0f172a;">{total_rute} Jalur</strong></div>', unsafe_allow_html=True)
    
    # 2. Boks Visualisasi Graph Utama
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    # Tampilkan Banner Rute Tercepat di atas Peta Graf jika ada rute
    if rute_tercepat_asal and jarak_terpendek != float('inf'):
        st.markdown(f"""
        <div class="fastest-card">
            <span style="color: #b91c1c; font-weight: 700; font-size: 13px;">🚀 RUTE TERCEPAT SAAT INI</span><br>
            <strong style="color: #991b1b; font-size: 16px;">{rute_tercepat_asal} ↔️ {rute_tercepat_tujuan} ({jarak_terpendek} km)</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Mempersiapkan Konfigurasi Node dan Edge untuk JavaScript Vis.js
    vis_nodes = []
    vis_edges = []
    
    for kota in graph.keys():
        if kota == hub_terbanyak and len(graph[kota]) > 0:
            vis_nodes.append({"id": kota, "label": f"⭐ {kota}\n(HUB UTAMA)", "color": {"background": "#f59e0b", "border": "#d97706"}, "font": {"color": "#ffffff", "size": 13, "bold": True}, "size": 26})
        else:
            vis_nodes.append({"id": kota, "label": kota, "color": {"background": "#3b82f6", "border": "#1d4ed8"}, "font": {"color": "#ffffff", "size": 12}, "size": 18})
            
    rute_tercatat = set()
    for kota_asal, tujuan_dict in graph.items():
        for kota_tujuan, jarak in tujuan_dict.items():
            rute_id = tuple(sorted([kota_asal, kota_tujuan]))
            if rute_id not in rute_tercatat:
                rute_tercatat.add(rute_id)
                
                # Cek apakah rute ini adalah rute tercepat
                is_tercepat = (kota_asal == rute_tercepat_asal and kota_tujuan == rute_tercepat_tujuan) or \
                             (kota_asal == rute_tercepat_tujuan and kota_tujuan == rute_tercepat_asal)
                
                if is_tercepat:
                    vis_edges.append({"from": kota_asal, "to": kota_tujuan, "label": f"🚀 {jarak} km", "color": {"color": "#ef4444", "highlight": "#dc2626"}, "width": 4, "font": {"color": "#b91c1c", "strokeWidth": 2, "strokeColor": "#ffffff"}})
                else:
                    vis_edges.append({"from": kota_asal, "to": kota_tujuan, "label": f"{jarak} km", "color": {"color": "#cbd5e1", "highlight": "#94a3b8"}, "width": 1.5, "font": {"color": "#475569"}})

    # Script HTML Vis.js
    html_code = f"""
    <div id="network-layout" style="width: 100%; height: 420px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff;"></div>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(vis_nodes)});
        var edges = new vis.DataSet({json.dumps(vis_edges)});
        var container = document.getElementById('network-layout');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
            nodes: {{ shape: 'dot', font: {{ face: 'Inter' }} }},
            edges: {{ font: {{ align: 'horizontal' }} }},
            physics: {{ stabilization: true, barnesHut: {{ gravitationalConstant: -1800, springLength: 140 }} }}
        }};
        var network = new vis.Network(container, data, options);
    </script>
    """
    
    # Jalankan Peta Jaringan
    components.html(html_code, height=440)
    
    # Legenda Peta
    st.markdown("""
    <div style="background-color: #f1f5f9; padding: 12px; border-radius: 8px; font-size: 13px; color: #475569;">
        <strong>💡 Panduan Navigasi Radar:</strong><br>
        • Kota berwarna <span style="color:#d97706; font-weight:bold;">Kuning (⭐)</span> berstatus sebagai pusat penghubung (Hub) logistik terpadat.<br>
        • Jalur berwarna <span style="color:#ef4444; font-weight:bold;">Merah Tebal (🚀)</span> adalah rute operasional langsung dengan jarak tempuh paling efisien/tercepat.<br>
        • Anda bisa melakukan <em>zoom in/out</em> serta menggeser posisi kota secara fleksibel pada kanvas.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

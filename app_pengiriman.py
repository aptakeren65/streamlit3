import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# Konfigurasi Halaman Mode Lebar & Judul Aplikasi
st.set_page_config(layout="wide", page_title="LOGIX - Route Graph Navigator", page_icon="🚀")

# ==========================================
# 🎨 KUSTOMISASI CSS: ULTRA DARK DASHBOARD MODE
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
        
        /* Font Global Modern */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            color: #f1f5f9;
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
            color: #94a3b8;
            border: 1px solid #334155;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2563eb !important;
            color: white !important;
            border-bottom: none !important;
        }
        
        /* Mempercantik Input Teks & Select Box */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #0f172a !important;
            color: #f1f5f9 !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
        }
        
        /* Tombol Utama (Confirm Button) */
        .stButton button {
            background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important;
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
        "São Paulo": {"Rio de Janeiro": 430, "Curitiba": 408, "Belo Horizonte": 586},
        "Rio de Janeiro": {"São Paulo": 430, "Belo Horizonte": 440},
        "Curitiba": {"São Paulo": 408, "Stops": 150},
        "Belo Horizonte": {"São Paulo": 586, "Rio de Janeiro": 440},
        "Stops": {"Curitiba": 150, "São Paulo": 280}
    }

graph = st.session_state.graph

# ==========================================
# 📊 LOGIKA OPERASIONAL GRAPH
# ==========================================
# Menemukan Hub Utama (Rute terbanyak)
hub_terbanyak = ""
maks_rute = 0
for kota, rute in graph.items():
    if len(rute) > maks_rute:
        maks_rute = len(rute)
        hub_terbanyak = kota

# Menemukan Rute Langsung Tercepat (Jarak Terpendek)
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

# Top Header Aplikasi
st.markdown("<h1 style='text-align: center; color: #ffffff; font-weight: 800; font-size: 36px; margin-bottom:0;'>🚀 LOGIX - Route Graph Navigator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px; margin-top:5px; margin-bottom:40px;'>Sistema de Gestão de Nodes e Rotas de Distribuição Logística Perusahaan</p>", unsafe_allow_html=True)

# Membagi Layar Menjadi Dua Panel Utama (Kiri: CRUD & Manifes | Kanan: Radar Maps)
kolom_kiri, kolom_kanan = st.columns([1, 1.4], gap="large")

# ------------------------------------------
# ⚙️ KOLOM KIRI: PAINEL DE GESTÃO (CRUD)
# ------------------------------------------
with kolom_kiri:
    st.markdown("<h4 style='color: #94a3b8; margin-bottom: 12px;'>⚙️ Painel de Gestão e CRUD</h4>", unsafe_allow_html=True)
    
    # Bungkus Panel ke dalam Box Card Aplikasi
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["➕ ADICIONAR DADO", "🔄 ATUALIZAR DISTÂNCIA", "❌ APAGAR DADO"])
    
    # Tab 1: Create
    with tab1:
        st.write("##")
        pilihan_input = st.radio("Pilih Jenis Komponen:", ["Node da Cidade (Kota)", "Rota Entre Cidades (Rute)"], horizontal=True)
        st.write("---")
        
        if pilihan_input == "Node da Cidade (Kota)":
            kota_baru = st.text_input("Nome da Nova Cidade (Nama Kota Baru)", placeholder="Contoh: Curitiba").strip()
            if st.button("Confirmar Registro (Simpan Kota)", use_container_width=True):
                if kota_baru and kota_baru not in graph:
                    graph[kota_baru] = {}
                    st.success(f"Kota {kota_baru} Berhasil Terdaftar!")
                    st.rerun()
        else:
            daftar_kota = list(graph.keys())
            if len(daftar_kota) >= 2:
                asal = st.selectbox("Origem (Kota Asal)", daftar_kota, key="c_asal")
                tujuan = st.selectbox("Destino (Kota Tujuan)", daftar_kota, key="c_tuj")
                jarak = st.number_input("Jarak (km)", min_value=1, value=100)
                if st.button("Confirmar Registro (Simpan Rute)", use_container_width=True):
                    if asal != tujuan:
                        graph[asal][tujuan] = jarak
                        graph[tujuan][asal] = jarak
                        st.success("Rute Berhasil Dihubungkan!")
                        st.rerun()
    
    # Tab 2: Update
    with tab2:
        st.write("##")
        daftar_kota = list(graph.keys())
        asal_up = st.selectbox("Origem (Kota Asal)", daftar_kota, key="u_asal")
        rute_ada = list(graph.get(asal_up, {}).keys())
        if rute_ada:
            tujuan_up = st.selectbox("Destino (Kota Tujuan)", rute_ada, key="u_tuj")
            jarak_baru = st.number_input("Jarak Baru (km)", min_value=1, value=int(graph[asal_up][tujuan_up]))
            if st.button("Atualizar (Update Jarak)", use_container_width=True):
                graph[asal_up][tujuan_up] = jarak_baru
                graph[tujuan_up][asal_up] = jarak_baru
                st.success("Jarak Rute Berhasil Diperbarui!")
                st.rerun()
        else:
            st.info("Kota ini belum memiliki rute.")

    # Tab 3: Delete
    with tab3:
        st.write("##")
        daftar_kota = list(graph.keys())
        kota_del = st.selectbox("Pilih Kota yang Akan Dihapus", daftar_kota, key="d_kota")
        if st.button("Apagar Dado (Hapus Kota Total)", type="primary", use_container_width=True):
            for tetangga in list(graph[kota_del].keys()):
                del graph[tetangga][kota_del]
            del graph[kota_del]
            st.success("Data Kota Berhasil Dihapus!")
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Info Manifest Mini Panel di bawah CRUD
    st.markdown("<h4 style='color: #94a3b8; margin-bottom: 12px;'>📋 Manifesto de Dados de Rota (Live)</h4>", unsafe_allow_html=True)
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    with col_inf1:
        st.markdown(f'<div class="custom-card" style="text-align:center; padding:15px;"><span style="color:#64748b; font-size:12px;">NODES TOTAIS</span><br><strong style="font-size:24px; color:#3b82f6;">{total_kota}</strong></div>', unsafe_allow_html=True)
    with col_inf2:
        st.markdown(f'<div class="custom-card" style="text-align:center; padding:15px;"><span style="color:#64748b; font-size:12px;">ROTAS TOTAIS</span><br><strong style="font-size:24px; color:#10b981;">{total_rute}</strong></div>', unsafe_allow_html=True)
    with col_inf3:
        st.markdown(f'<div class="custom-card" style="text-align:center; padding:15px;"><span style="color:#64748b; font-size:12px;">OPERASI UTAMA</span><br><strong style="font-size:14px; color:#f59e0b;">{hub_terbanyak}</strong></div>', unsafe_allow_html=True)

# ------------------------------------------
# 🗺️ KOLOM KANAN: RADAR MAPS REAL-TIME
# ------------------------------------------
with kolom_kanan:
    st.markdown("<h4 style='color: #94a3b8; margin-bottom: 12px;'>🗺️ Mapa Interaktif de Rede (Radar Real-time)</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card" style="background-color: #0b1329;">', unsafe_allow_html=True)
    
    # 3 Kotak Indikator Mini di Atas Gambar Peta
    col_ind1, col_ind2, col_ind3 = st.columns(3)
    with col_ind1:
        st.markdown(f'<p style="color:#64748b; font-size:11px; margin-bottom:2px;">TOTAL DE CIDADES (NODES)</p><h5 style="color:#ffffff; margin-top:0;">👥 {total_kota} Cidades</h5>', unsafe_allow_html=True)
    with col_ind2:
        st.markdown(f'<p style="color:#64748b; font-size:11px; margin-bottom:2px;">TOTAL DE ROTAS (EDGES)</p><h5 style="color:#ffffff; margin-top:0;">🔀 {total_rute} Rotas</h5>', unsafe_allow_html=True)
    with col_ind3:
        if rute_tercepat_asal:
            st.markdown(f'<p style="color:#ef4444; font-size:11px; margin-bottom:2px; font-weight:bold;">🚀 ROTA MAIS EFICIENTE ATUAL</p><h5 style="color:#ffffff; margin-top:0;">{rute_tercepat_asal} → {rute_tercepat_tujuan}</h5>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#64748b; font-size:11px; margin-bottom:2px;">ROTA MAIS EFICIENTE ATUAL</p><h5 style="color:#ffffff; margin-top:0;">-</h5>', unsafe_allow_html=True)
            
    st.write("---")
    
    # Menyiapkan data Node & Edge JSON untuk JavaScript Vis.js (Tema Glow-Dark)
    vis_nodes = []
    vis_edges = []
    
    for kota in graph.keys():
        if kota == hub_terbanyak:
            vis_nodes.append({"id": kota, "label": f"⭐ {kota}\n(HUB)", "color": {"background": "#f59e0b", "border": "#d97706"}, "font": {"color": "#ffffff", "size": 13, "bold": True}, "size": 25})
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
    st.markdown("<p style='color: #64748b; font-size: 12px; text-align: center; margin-top:10px;'>⚡ ROTA MAIS RÁPIDA (🚀 TERCEPAT) di-highlight dengan jalur merah menyala secara real-time.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

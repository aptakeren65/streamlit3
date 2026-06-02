import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# Konfigurasi Halaman Mode Lebar & Judul Aplikasi
st.set_page_config(layout="wide", page_title="LOGIX - Navigator Rute Jaringan", page_icon="🚀")

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
        "Jakarta": {"Bandung": 150, "Semarang": 450, "Surabaya": 780},
        "Bandung": {"Jakarta": 150, "Yogyakarta": 400},
        "Semarang": {"Jakarta": 450, "Yogyakarta": 120, "Surabaya": 350},
        "Surabaya": {"Jakarta": 780, "Semarang": 350},
        "Yogyakarta": {"Bandung": 400, "Semarang": 120}
    }

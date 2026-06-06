import streamlit as st
import math

# ==========================================
# 1. PENGATURAN HALAMAN
# ==========================================
st.set_page_config(
    page_title="Kalkulator Analisis Kuantitatif",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. FUNGSI UNTUK MENAMPILKAN KARTU HASIL (FIXED NAMEERROR)
# ==========================================
def res(label, value, unit=""):
    """Fungsi untuk membuat komponen kartu hasil perhitungan yang estetik"""
    return f"""
    <div class="result-card">
        <p class="result-label">{label}</p>
        <p class="result-value">{value} <span style="font-size:16px; color:#00e5ff;">{unit}</span></p>
    </div>
    """

# ==========================================
# 3. GAYA CSS CUSTOM (TEMA BIRU GELAP LABORATORIUM - FIXED TEXT COLOR)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* Mengubah background utama aplikasi menjadi Gelap Lab */
.stApp {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%) !important;
    background-attachment: fixed;
    color: #ffffff !important;
}

html, body, [class*="css"] { 
    font-family: 'DM Sans', sans-serif; 
}

/* Memaksa teks label di luar box tetap berwarna putih */
.stMarkdown, p, label, .stSlider, .stRadio, div[data-baseweb="checkbox"] {
    color: #ffffff !important;
}

/* FIX: Memaksa teks di dalam INPUT BOX, SELECTBOX, dan TEXTAREA menjadi GELAP agar terbaca jelas */
div[data-testid="stNumberInput"] input, 
div[data-testid="stTextInput"] input, 
div[data-testid="stTextArea"] textarea,
div[data-baseweb="select"] div {
    color: #1a252c !important; /* Warna abu-abu gelap mendekati hitam */
    font-weight: 500 !important;
}

/* FIX: Mengubah teks pilihan di dalam Dropdown Menu saat diklik agar tetap gelap */
div[data-shaded="true"], ul[role="listbox"] li {
    color: #1a252c !important;
}

/* FIX: Menyesuaikan warna teks pada komponen Tabs (Navigasi Modul) */
button[data-baseweb="tab"] p {
    color: #b0bec5 !important; /* Warna teks tab yang tidak aktif */
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #00e5ff !important; /* Warna teks tab aktif (Cyan Neon) */
    font-weight: bold !important;
}

/* Badge di atas judul */
.badge { 
    display:inline-block; font-family:'DM Mono',monospace; font-size:11px; font-weight:500;
    letter-spacing:.08em; text-transform:uppercase; color:#00e5ff; border:1px solid #00e5ff;
    border-radius:999px; padding:4px 14px; margin-bottom:1rem; background: rgba(0, 229, 255, 0.1);
}

/* Judul Utama Dashboard */
.main-title { 
    font-family:'DM Serif Display',serif; font-size:42px; line-height:1.15; color:#ffffff; margin:0 0 .5rem;
}
.main-title em { 
    font-style:italic; color:#00e5ff; 
}
.subtitle { 
    font-size:15px; color:#b0bec5; line-height:1.6; max-width:600px; margin-bottom:1.5rem; 
}

/* Kotak Rumus */
.formula-box { 
    background: rgba(255, 255, 255, 0.05); border:1px solid #00e5ff; border-radius:10px; padding:12px 16px;
    font-family:'DM Mono',monospace; font-size:13px; color:#00e5ff; text-align:center; margin:1rem 0; 
}

/* STYLE HALAMAN PEMBUKA (START PAGE) */
.welcome-outer {
    max-width: 750px;
    margin: 3rem auto 2rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,229,255,0.15);
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
}

.welcome-header {
    background: linear-gradient(135deg, #00e5ff, #2c5364);
    padding: 2.5rem;
    text-align: center;
    color: white;
}
.welcome-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 40px;
    margin: 0;
    letter-spacing: 0.5px;
    text-shadow: 1px 2px 4px rgba(0,0,0,0.3);
}

.welcome-body {
    padding: 2.5rem 2rem;
    text-align: center;
    color: #ffffff;
}
.welcome-desc {
    font-size: 22px;
    font-weight: 500;
    line-height: 1.5;
    margin: 0 auto;
    max-width: 600px;
}

/* Blok Info Tujuan & Manfaat */
.info-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    height: 100%;
    border: 1px solid rgba(255,255,255,0.05);
}
.info-card-tujuan { border-top: 5px solid #00e5ff; }
.info-card-manfaat { border-top: 5px solid #00e5ff; }

.info-card h4 {
    margin-top: 0;
    font-size: 18px;
    margin-bottom: 0.75rem;
    color: #00e5ff;
}
.info-card ul {
    margin: 0;
    padding-left: 1.2rem;
    font-size: 14px;
    color: #cfd8dc;
    line-height: 1.6;
}

/* Style untuk Kartu Menu Utama Dashboard */
.menu-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.5rem;
    height: 200px;
    transition: all 0.2s ease;
    border: 1px solid rgba(255,255,255,0.05);
}
.card-p1 { border-left: 5px solid #00e5ff; }
.card-p2 { border-left: 5px solid #00dbde; }
.card-p3 { border-left: 5px solid #fc00ff; }
.card-p4 { border-left: 5px solid #00ff87; }
.card-p5 { border-left: 5px solid #ff007f; }

.menu-card:hover {
    box-shadow: 0 8px 20px rgba(0, 229, 255, 0.2);
    transform: translateY(-3px);
    background: rgba(255, 255, 255, 0.08);
}
.menu-icon { font-size: 24px; margin-bottom: 0.5rem; }
.menu-title { font-size: 18px; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0.5rem; color: #ffffff; }
.menu-desc { font-size: 13px; color: #b0bec5; line-height: 1.5; }

/* Custom Tombol Utama */
div.stButton > button {
    background: linear-gradient(135deg, #00e5ff, #00dbde) !important;
    color: #0f2027 !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: bold !important;
    box-shadow: 0 4px 10px rgba(0, 229, 255, 0.3) !important;
    transition: all 0.2s;
}
div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 15px rgba(0, 229, 255, 0.6) !important;
    background: linear-gradient(135deg, #ffffff, #00e5ff) !important;
}

/* Style Kartu Hasil */
.result-card { 
    background: rgba(255, 255, 255, 0.05); border-radius:12px; padding:1rem 1.4rem; margin-top:.75rem; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.3); border: 1px solid rgba(0, 229, 255, 0.2); 
}
.result-label { font-size:11px; font-family:'DM Mono',monospace; text-transform:uppercase; letter-spacing:.07em; margin:0 0 4px; color: #b0bec5; }
.result-value { font-size:26px; font-weight:500; margin:0; font-family:'DM Mono',monospace; color: #00e5ff; }

/* Menambahkan elemen rumus kimia dekoratif transparan melayang di background */
.stApp::before {
    content: "🧪  ⚗️  ⚛️  H₂O  CO₂  NaCl  M₁V₁=M₂V₂  pH=-log[H⁺]  🧫  NaOH  HCl";
    position: fixed;
    top: 15%;
    left: 5%;
    font-size: 4.5rem;
    font-family: 'Courier New', monospace;
    opacity: 0.03; 
    white-space: pre-wrap;
    word-spacing: 50px;
    line-height: 2.8;
    pointer-events: none;
    width: 90%;
    z-index: 0;
}
}

/* Style untuk Kartu Menu Utama Dashboard */
.menu-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.5rem;
    height: 200px;
    transition: all 0.2s ease;
    border: 1px solid rgba(255,255,255,0.05);
}
.card-p1 { border-left: 5px solid #00e5ff; }
.card-p2 { border-left: 5px solid #00dbde; }
.card-p3 { border-left: 5px solid #fc00ff; }
.card-p4 { border-left: 5px solid #00ff87; }
.card-p5 { border-left: 5px solid #ff007f; }

.menu-card:hover {
    box-shadow: 0 8px 20px rgba(0, 229, 255, 0.2);
    transform: translateY(-3px);
    background: rgba(255, 255, 255, 0.08);
}
.menu-icon { font-size: 24px; margin-bottom: 0.5rem; }
.menu-title { font-size: 18px; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0.5rem; color: #ffffff; }
.menu-desc { font-size: 13px; color: #b0bec5; line-height: 1.5; }

/* Custom Mengubah Box Input (Number, Text, Selectbox) bawaan Streamlit agar serasi dengan Tema Gelap */
div[data-testid="stNumberInput"], div[data-testid="stSelectbox"], div[data-testid="stTextInput"], div[data-testid="stTextArea"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px !important;
    color: white !important;
}
input, select, textarea {
    color: white !important;
}

/* Custom Tombol agar berwarna Cyber Cyan/Neon */
div.stButton > button {
    background: linear-gradient(135deg, #00e5ff, #00dbde) !important;
    color: #0f2027 !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: bold !important;
    box-shadow: 0 4px 10px rgba(0, 229, 255, 0.3) !important;
    transition: all 0.2s;
}
div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 15px rgba(0, 229, 255, 0.6) !important;
    background: linear-gradient(135deg, #ffffff, #00e5ff) !important;
}

/* Style Kartu Hasil */
.result-card { 
    background: rgba(255, 255, 255, 0.05); border-radius:12px; padding:1rem 1.4rem; margin-top:.75rem; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.3); border: 1px solid rgba(0, 229, 255, 0.2); 
}
.result-label { font-size:11px; font-family:'DM Mono',monospace; text-transform:uppercase; letter-spacing:.07em; margin:0 0 4px; color: #b0bec5; }
.result-value { font-size:26px; font-weight:500; margin:0; font-family:'DM Mono',monospace; color: #00e5ff; }

/* Menambahkan elemen rumus kimia dekoratif transparan melayang di background */
.stApp::before {
    content: "🧪  ⚗️  ⚛️  H₂O  CO₂  NaCl  M₁V₁=M₂V₂  pH=-log[H⁺]  🧫  NaOH  HCl";
    position: fixed;
    top: 15%;
    left: 5%;
    font-size: 4.5rem;
    font-family: 'Courier New', monospace;
    opacity: 0.03; /* Dibuat samar agar tulisan depan tetap terbaca jernih */
    white-space: pre-wrap;
    word-spacing: 50px;
    line-height: 2.8;
    pointer-events: none;
    width: 90%;
    z-index: 0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. STATE MANAGEMENT NAVIGASI
# ==========================================
if 'menu_aktif' not in st.session_state:
    st.session_state.menu_aktif = "Start"

def pindah_ke(nama_modul):
    st.session_state.menu_aktif = nama_modul

SATUAN_KONSENTRASI = ["Molaritas (M)", "% massa/volume (% m/v)", "ppm (mg/L)", "ppb (µg/L)", "mg/mL", "Molalitas (m)"]

def to_mgL(val, sat, mr, rho=1.0):
    tabel = {"Molaritas (M)": val*mr*1000, "% massa/volume (% m/v)": val*10000, "ppm (mg/L)": val, "ppb (µg/L)": val/1000, "mg/mL": val*1000, "Molalitas (m)": val*mr*rho*1000}
    return tabel.get(sat, val)

def from_mgL(mgL, sat, mr, rho=1.0):
    tabel = {"Molaritas (M)": mgL/(mr*1000), "% massa/volume (% m/v)": mgL/10000, "ppm (mg/L)": mgL, "ppb (µg/L)": mgL*1000, "mg/mL": mgL/1000, "Molalitas (m)": mgL/(mr*rho*1000)}
    return tabel.get(sat, mgL)


# ==========================================
# 5. HALAMAN ISI KONTEN
# ==========================================

# --- HALAMAN PEMBUKA (START PAGE) ---
if st.session_state.menu_aktif == "Start":
    st.markdown("""
    <div class="welcome-outer">
        <div class="welcome-header">
            <h1>Selamat Datang</h1>
        </div>
        <div class="welcome-body">
            <p class="welcome-desc">Aplikasi Kalkulator Kimia Analitik Kuantitatif</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1.2, 1, 1.2])
    with col_btn:
        if st.button("🌟 Masuk ke Aplikasi", key="btn_start", use_container_width=True):
            pindah_ke("Dashboard")
            st.rerun()
            
    st.write("<br><br>", unsafe_allow_html=True)
    
    col_tujuan, col_manfaat = st.columns(2)
    with col_tujuan:
        st.markdown("""
        <div class="info-card info-card-tujuan">
            <h4>🎨 Tujuan Aplikasi</h4>
            <ul>
                <li>Menyediakan platform hitung laboratorium modern yang menyenangkan dan mudah dipahami.</li>
                <li>Mengecek kekeliruan pengerjaan angka desimal berkat otomasi kalkulasi analitis.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_manfaat:
        st.markdown("""
        <div class="info-card info-card-manfaat">
            <h4>✨ Manfaat Aplikasi</h4>
            <ul>
                <li><b>Cepat & Efisien:</b> Memproses rumus C1V1=V2C2 dan hitungan stoikiometri dalam hitungan detik.</li>
                <li><b>Visual & Akurat:</b> Dilengkapi pelacakan rumus transparan serta alat hitung galat deviasi (SD/RSD).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- HALAMAN MENU UTAMA (DASHBOARD KARTU) ---
elif st.session_state.menu_aktif == "Dashboard":
    st.markdown('<div class="badge">🧪Kimia Analitik</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 class="main-title">Kalkulator <em>Analisis</em> Kuantitatif</h1>
    <p class="subtitle">Silakan pilih salah satu modul kalkulator ceria di bawah ini untuk memulai:</p>
    """, unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="menu-card card-p1"><div class="menu-icon">💧</div><div class="menu-title">Pengenceran Larutan</div><div class="menu-desc">Kalkulator pengenceran tunggal, serial/bertingkat, dan penentuan faktor pengenceran sampel.</div></div>', unsafe_allow_html=True)
        if st.button("Buka Modul 01 ➡️", key="btn_m1", use_container_width=True): 
            pindah_ke("Pengenceran")
            st.rerun()
    with col2:
        st.markdown('<div class="menu-card card-p2"><div class="menu-icon">🔄</div><div class="menu-title">Konsentrasi & Stoikiometri</div><div class="menu-desc">Fitur konversi otomatis antar satuan kimia (M, %, ppm, ppb) dan hitung stoikiometri reaksi mol.</div></div>', unsafe_allow_html=True)
        if st.button("Buka Modul 02 ➡️", key="btn_m2", use_container_width=True): 
            pindah_ke("Stoikiometri")
            st.rerun()
    with col3:
        st.markdown('<div class="menu-card card-p3"><div class="menu-icon">🌈</div><div class="menu-title">Kesetimbangan & pH</div><div class="menu-desc">Prediksi nilai keasaman (pH) sistem asam-basa kuat/lemah serta perhitungan nilai Ka/Kb tetapan larutan.</div></div>', unsafe_allow_html=True)
        if st.button("Buka Modul 03 ➡️", key="btn_m3", use_container_width=True): 
            pindah_ke("pH")
            st.rerun()

    st.write("")
    col4, col5, _ = st.columns(3)
    with col4:
        st.markdown('<div class="menu-card card-p4"><div class="menu-icon">🧪</div><div class="menu-title">Larutan Buffer</div><div class="menu-desc">Desain pembuatan sistem larutan penyangga menggunakan persamaan Henderson-Hasselbalch.</div></div>', unsafe_allow_html=True)
        if st.button("Buka Modul 04 ➡️", key="btn_m4", use_container_width=True): 
            pindah_ke("Buffer")
            st.rerun()
    with col5:
        st.markdown('<div class="menu-card card-p5"><div class="menu-icon">📊</div><div class="menu-title">Galat & Propagasi</div><div class="menu-desc">Komputasi nilai ketidakpastian sistem matematika lab, deviasi standar (SD), dan nilai RSD data.</div></div>', unsafe_allow_html=True)
        if st.button("Buka Modul 05 ➡️", key="btn_m5", use_container_width=True): 
            pindah_ke("Galat")
            st.rerun()

# --- HALAMAN MODUL KALKULATOR AKTIF ---
else:
    if st.button("⬅️ Kembali ke Menu Utama", key="btn_kembali"):
        pindah_ke("Dashboard")
        st.rerun()
    st.divider()

    # MODUL 1 — PENGENCERAN
    if st.session_state.menu_aktif == "Pengenceran":
        st.markdown("### 💧 Pengenceran Larutan")
        t1a, t1b, t1c = st.tabs(["C₁V₁ = C₂V₂", "Serial / Bertingkat", "Faktor Pengenceran"])
        with t1a:
            st.markdown('<div class="formula-box">C₁ × V₁ = C₂ × V₂</div>', unsafe_allow_html=True)
            cari = st.selectbox("Variabel yang dicari:", ["C₂ — Konsentrasi akhir","V₂ — Volume akhir","C₁ — Konsentrasi awal","V₁ — Volume awal"], key="e_cari")
            satuan = st.selectbox("Satuan konsentrasi:", ["M","mM","µM","mg/mL","ppm","ppb"], key="e_sat")
            col1, col2 = st.columns(2)
            if cari == "C₂ — Konsentrasi akhir":
                with col1:
                    c1 = st.number_input("C₁ — Konsentrasi awal", 0.0, value=1.0, format="%.5f", key="ec1a")
                    v1 = st.number_input("V₁ — Volume awal (mL)",  0.0, value=10.0, format="%.3f", key="ev1a")
                with col2: v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, format="%.3f", key="ev2a")
                hasil = (c1*v1)/v2
                st.markdown(res("C₂ — Konsentrasi akhir", f"{hasil:.6g}", satuan), unsafe_allow_html=True)
            elif cari == "V₂ — Volume akhir":
                with col1:
                    c1 = st.number_input("C₁ — Konsentrasi awal", 0.0, value=1.0, format="%.5f", key="ec1b")
                    v1 = st.number_input("V₁ — Volume awal (mL)",  0.0, value=10.0, format="%.3f", key="ev1b")
                with col2: c2 = st.number_input("C₂ — Konsentrasi akhir", 1e-9, value=0.1, format="%.5f", key="ec2b")
                hasil = (c1*v1)/c2
                st.markdown(res("V₂ — Volume akhir", f"{hasil:.5g}", "mL"), unsafe_allow_html=True)
            elif cari == "C₁ — Konsentrasi awal":
                with col1:
                    v1 = st.number_input("V₁ — Volume awal (mL)",  1e-9, value=10.0, format="%.3f", key="ev1c")
                    c2 = st.number_input("C₂ — Konsentrasi akhir", 0.0,  value=0.1, format="%.5f", key="ec2c")
                with col2: v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, format="%.3f", key="ev2c")
                hasil = (c2*v2)/v1
                st.markdown(res("C₁ — Konsentrasi awal", f"{hasil:.6g}", satuan), unsafe_allow_html=True)
            else:
                with col1:
                    c1 = st.number_input("C₁ — Konsentrasi awal", 1e-9, value=1.0, format="%.5f", key="ec1d")
                    c2 = st.number_input("C₂ — Konsentrasi akhir", 0.0, value=0.1, format="%.5f", key="ec2d")
                with col2: v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, format="%.3f", key="ev2d")
                hasil = (c2*v2)/c1
                st.markdown(res("V₁ — Volume awal", f"{hasil:.5g}", "mL"), unsafe_allow_html=True)
        with t1b:
            st.markdown('<div class="formula-box">C₢ = C₀ × (V_aliquot / V_total)ⁿ</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                c0 = st.number_input("C₀ — Konsentrasi stok", 0.0, value=1.0, format="%.5f", key="s_c0")
                nstep = st.number_input("Jumlah langkah", 1, 15, value=5, key="s_n")
            with col2:
                va_s = st.number_input("Volume aliquot (mL)", 0.001, value=1.0, format="%.3f", key="s_va")
                vt_s = st.number_input("Volume total tiap tabung (mL)", 0.001, value=10.0, format="%.3f", key="s_vt")
                sat_s = st.selectbox("Satuan", ["M","mM","µM","mg/mL","ppm"], key="s_sat")
            if va_s >= vt_s: st.warning("Volume aliquot harus lebih kecil dari volume total.")
            else:
                f = va_s / vt_s
                rows = "".join(f"<tr><td style='padding:6px 10px; border-bottom:1px solid rgba(255,255,255,0.1)'>{'Stok' if i==0 else f'Langkah {i}'}</td><td style='padding:6px 10px;font-family:DM Mono,monospace;color:#00e5ff; border-bottom:1px solid rgba(255,255,255,0.1)'>{c0*(f**i):.4e}</td><td style='padding:6px 10px;color:#b0bec5; border-bottom:1px solid rgba(255,255,255,0.1)'>{sat_s}</td></tr>" for i in range(int(nstep)+1))
                st.markdown(f"""<table style="width:100%;border-collapse:collapse;border:1px solid rgba(0,229,255,0.2);font-size:13px;margin-top:.5rem;background:rgba(255,255,255,0.05);border-radius:10px;overflow:hidden"><thead><tr style="background:rgba(0,229,255,0.1)"><th style="padding:8px 10px;text-align:left;color:#00e5ff">Tabung</th><th style="padding:8px 10px;text-align:left;color:#00e5ff">Konsentrasi</th><th style="padding:8px 10px;text-align:left;color:#00e5ff">Satuan</th></tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)
        with t1c:
            col1, col2 = st.columns(2)
            with col1:
                va_fp = st.number_input("Volume awal (mL)",  0.001, value=1.0, format="%.3f", key="fp_va")
                vb_fp = st.number_input("Volume akhir (mL)", 0.001, value=100.0, format="%.3f", key="fp_vb")
            with col2: ca_fp = st.number_input("Konsentrasi awal (opsional)", 0.0, value=1.0, format="%.5f", key="fp_ca")
            fp = vb_fp / va_fp
            st.markdown(res("Faktor Pengenceran", f"1 : {fp:.4f}", ""), unsafe_allow_html=True)
            st.markdown(res("Konsentrasi Akhir", f"{ca_fp/fp:.5g}", ""), unsafe_allow_html=True)

    # MODUL 2 — STOIKIOMETRI
    elif st.session_state.menu_aktif == "Stoikiometri":
        st.markdown("### 🔄 Satuan Konsentrasi & Stoikiometri")
        t2a, t2b, t2c = st.tabs(["🔄 Konversi Satuan", "⚖️ Mol & Massa", "🧮 Stoikiometri Reaksi"])
        with t2a:
            col1, col2 = st.columns(2)
            with col1:
                dari = st.selectbox("Dari satuan:", SATUAN_KONSENTRASI, index=0, key="k_dari")
                nilai = st.number_input("Nilai", 0.0, value=1.0, format="%.6f", key="k_val")
                mr_k = st.number_input("Mr zat (g/mol)", 0.001, value=58.44, key="k_mr")
            with col2:
                ke = st.selectbox("Ke satuan:", SATUAN_KONSENTRASI, index=2, key="k_ke")
                rho = st.number_input("Densitas ρ (g/mL)", 0.001, value=1.0, key="k_rho")
            if dari == ke: st.warning("Pilih satuan yang berbeda.")
            else:
                mgL = to_mgL(nilai, dari, mr_k, rho)
                hasil = from_mgL(mgL, ke, mr_k, rho)
                st.markdown(res("Hasil Konversi", f"{hasil:.6g}", ke), unsafe_allow_html=True)
        with t2b:
            cari_m = st.selectbox("Cari:", ["Mol (n) dari massa & Mr","Mol (n) dari M & V","Massa (g) dari n & Mr","Molaritas (M) dari n & V","Volume (mL) dari n & M"], key="mol_cari")
            col1, col2 = st.columns(2)
            if "massa" in cari_m:
                with col1: massa = st.number_input("Massa (gram)", 0.0, value=5.85, format="%.4f", key="mol_ma")
                with col2: mr2 = st.number_input("Mr (g/mol)", 0.001, value=58.44, key="mol_mr")
                st.markdown(res("Mol (n)", f"{massa/mr2:.5g}", "mol"), unsafe_allow_html=True)
            elif "M & V" in cari_m:
                with col1: Mm = st.number_input("Molaritas (M)", 0.0, value=1.0, key="mol_Mm")
                with col2: Vm = st.number_input("Volume (mL)", 0.0, value=100.0, key="mol_Vm")
                st.markdown(res("Mol (n)", f"{Mm*(Vm/1000):.5g}", "mol"), unsafe_allow_html=True)
            elif "Massa" in cari_m:
                with col1: nm = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_nm")
                with col2: mr3 = st.number_input("Mr (g/mol)", 0.001, value=58.44, key="mol_mr3")
                st.markdown(res("Massa (m)", f"{nm*mr3:.5g}", "gram"), unsafe_allow_html=True)
            elif "Molaritas" in cari_m:
                with col1: nm = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_nm2")
                with col2: Vm = st.number_input("Volume (mL)", 0.001, value=100.0, key="mol_Vm2")
                st.markdown(res("Molaritas (M)", f"{nm/(Vm/1000):.5g}", "mol/L"), unsafe_allow_html=True)
            else:
                with col1: nm = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_nm3")
                with col2: Mm = st.number_input("Molaritas (M)", 0.001, value=1.0, key="mol_Mm3")
                st.markdown(res("Volume (V)", f"{(nm/Mm)*1000:.5g}", "mL"), unsafe_allow_html=True)
        with t2c:
            col1, col2, col3, col4 = st.columns(4)
            with col1: kA, nA, mA = st.number_input("Koef A", 1, value=1), st.text_input("Nama A", "HCl"), st.number_input("Mr A", 0.001, value=36.46)
            with col2: kB, nB, mB = st.number_input("Koef B", 1, value=1), st.text_input("Nama B", "NaOH"), st.number_input("Mr B", 0.001, value=40.00)
            with col3: kC, nC, mC = st.number_input("Koef C", 1, value=1), st.text_input("Nama C", "NaCl"), st.number_input("Mr C", 0.001, value=58.44)
            with col4: kD, nD, mD = st.number_input("Koef D", 1, value=1), st.text_input("Nama D", "H₂O"), st.number_input("Mr D", 0.001, value=18.02)
            st.info(f"**Reaksi:** {kA} {nA} + {kB} {nB} → {kC} {nC} + {kD} {nD}")
            zat_r = st.selectbox("Reaktan pembatas:", [nA, nB])
            n_ref = st.number_input("Mol Reaktan Pembatas", 0.0, value=0.1)
            k_ref = kA if zat_r == nA else kB
            nC_mol = n_ref*(kC/k_ref)
            st.markdown(res(f"Hasil {nC}", f"{nC_mol:.5g} mol ({nC_mol*mC:.5g} g)", ""), unsafe_allow_html=True)

    # MODUL 3 — pH KESETIMBANGAN
    elif st.session_state.menu_aktif == "pH":
        st.markdown("### 🌈 Kesetimbangan & Perubahan pH")
        t3a, t3b, t3c, t3d = st.tabs(["🔴 pH Asam", "🔵 pH Basa", "🔬 Hitung Ka/Kb", "📉 ΔpH Pengenceran"])
        with t3a:
            jenis_a = st.radio("Jenis asam:", ["Asam Kuat","Asam Lemah"], horizontal=True)
            Ca = st.number_input("Konsentrasi C (M)", 1e-14, value=0.1, key="as_C")
            if jenis_a == "Asam Kuat": pH = -math.log10(max(Ca, 1e-14))
            else:
                Ka_a = st.number_input("Ka", 1e-20, value=1.8e-5, key="as_Ka")
                pH = -math.log10(math.sqrt(Ka_a * Ca))
            st.markdown(res("pH Larutan", f"{pH:.4f}", ""), unsafe_allow_html=True)
        with t3b:
            jenis_b = st.radio("Jenis basa:", ["Basa Kuat","Basa Lemah"], horizontal=True)
            Cb = st.number_input("Konsentrasi C (M)", 1e-14, value=0.1, key="bs_C")
            if jenis_b == "Basa Kuat": pH = 14 + math.log10(Cb)
            else:
                Kb_b = st.number_input("Kb", 1e-20, value=1.8e-5, key="bs_Kb")
                pH = 14 + math.log10(math.sqrt(Kb_b * Cb))
            st.markdown(res("pH Larutan", f"{pH:.4f}", ""), unsafe_allow_html=True)
        with t3c:
            Ck = st.number_input("Konsentrasi C (M)", 1e-10, value=0.1, key="kk_C")
            pHk = st.number_input("pH terukur", 0.0, 14.0, value=2.87, key="kk_pH")
            H = 10**(-pHk)
            if Ck > H: st.markdown(res("Ka Prediksi", f"{H**2 / (Ck - H):.4e}", ""), unsafe_allow_html=True)
        with t3d:
            jenis_d = st.radio("Jenis larutan:", ["Asam Kuat","Asam Lemah","Basa Kuat","Basa Lemah"], horizontal=True, key="dp_j")
            def c_ph(j, c, k=None):
                c = max(c, 1e-14)
                if j == "Asam Kuat": return -math.log10(c)
                if j == "Asam Lemah": return -math.log10(math.sqrt(k * c))
                if j == "Basa Kuat": return 14 + math.log10(c)
                if j == "Basa Lemah": return 14 + math.log10(math.sqrt(k * c))
            C1d = st.number_input("C₁ (M)", 1e-14, value=0.1, key="dp_C1")
            V1d = st.number_input("V₁ (mL)", 0.001, value=10.0, key="dp_V1")
            V2d = st.number_input("V₂ (mL)", 0.001, value=100.0, key="dp_V2")
            Kd = st.number_input("Ka / Kb", 1e-20, value=1.8e-5, key="dp_K") if "Lemah" in jenis_d else None
            pH1 = c_ph(jenis_d, C1d, Kd)
            pH2 = c_ph(jenis_d, (C1d*V1d/V2d), Kd)
            st.markdown(res("pH Akhir", f"{pH2:.4f} (Awal: {pH1:.4f})", ""), unsafe_allow_html=True)

    # MODUL 4 — LARUTAN BUFFER
    elif st.session_state.menu_aktif == "Buffer":
        st.markdown("### 🧪 Pembuatan Larutan Buffer")
        t4a, t4b, t4c = st.tabs(["🧮 Hitung pH Buffer", "⚖️ Hitung Rasio [A⁻]/[HA]", "📊 Kapasitas Buffer (β)"])
        with t4a:
            pKa_b = st.number_input("pKa asam", 0.0, 14.0, value=4.74)
            ab = st.number_input("[A⁻] Basa Konjugat (M)", 0.0001, value=0.1)
            ha = st.number_input("[HA] Asam (M)", 0.0001, value=0.1)
            st.markdown(res("pH Buffer", f"{pKa_b + math.log10(ab / ha):.4f}", ""), unsafe_allow_html=True)
        with t4b:
            pHt = st.number_input("pH target", 0.0, 14.0, value=5.0)
            pKa_r = st.number_input("pKa asam", 0.0, 14.0, value=4.74, key="br_pka")
            Ctot = st.number_input("Konsentrasi total (M)", 0.001, value=0.2)
            ratio = 10**(pHt - pKa_r)
            st.markdown(res("Rasio [A⁻]/[HA]", f"{ratio:.5f}", f"([A⁻]={Ctot*ratio/(1+ratio):.4f}M)"), unsafe_allow_html=True)
        with t4c:
            Cbc = st.number_input("Konsentrasi total (M)", 0.0001, value=0.1, key="bc_C")
            Ka_bc = st.number_input("Ka", 1e-20, value=1.8e-5, key="bc_Ka")
            pH_bc = st.number_input("pH larutan", 0.0, 14.0, value=4.74, key="bc_pH")
            H_bc = 10**(-pH_bc)
            beta = 2.303 * Cbc * (Ka_bc * H_bc) / (Ka_bc + H_bc)**2
            st.markdown(res("Kapasitas Buffer (β)", f"{beta:.4e}", ""), unsafe_allow_html=True)

    # MODUL 5 — ANALISIS GALAT
    elif st.session_state.menu_aktif == "Galat":
        st.markdown("### 📊 Galat & Propagasi Error")
        t5a, t5b, t5c = st.tabs(["📏 Galat Absolut & Relatif", "⚡ Propagasi Error", "📊 Statistik (SD & RSD)"])
        with t5a:
            xu = st.number_input("Nilai terukur", value=9.87)
            xb = st.number_input("Nilai benar", value=10.00)
            st.markdown(res("Galat Absolut", f"{abs(xu-xb):.5g}", ""), unsafe_allow_html=True)
        with t5b:
            op = st.selectbox("Operasi:", ["Penjumlahan / Pengurangan (x ± y)", "Perkalian / Pembagian (x × y atau x/y)"])
            x_val = st.number_input("Nilai x", value=10.0)
            dx_val = st.number_input("δx", value=0.05)
            y_val = st.number_input("Nilai y", value=5.0)
            dy_val = st.number_input("δy", value=0.03)
            if "Penjumlahan" in op: st.markdown(res("Ketidakpastian Akhir", f"± {math.sqrt(dx_val**2 + dy_val**2):.5g}", ""), unsafe_allow_html=True)
            else: st.markdown(res("Ketidakpastian Akhir", f"± {(x_val*y_val)*math.sqrt((dx_val/x_val)**2 + (dy_val/y_val)**2):.5g}", ""), unsafe_allow_html=True)
        with t5c:
            raw = st.text_area("Data pengukuran (pisahkan dengan koma):", value="9.87, 9.92, 9.85, 9.90, 9.88")
            arr = [float(t.strip()) for t in raw.split(',') if t.strip()]
            if len(arr) >= 2:
                mean_s = sum(arr)/len(arr)
                sd_s = math.sqrt(sum((xi-mean_s)**2 for xi in arr)/(len(arr)-1))
                st.markdown(res("Rata-rata ± SD", f"{mean_s:.4g} ± {sd_s:.4g}", f"(RSD: {sd_s/mean_s*100:.3f}%)"), unsafe_allow_html=True)

# ==========================================
# 6. FOOTER HALAMAN
# ==========================================
st.divider()
st.markdown('<p style="text-align:center;font-size:12px;color:#00e5ff;font-weight:500;">⚗️ Kalkulator Analisis Kuantitatif · Kimia Analitik</p>', unsafe_allow_html=True)

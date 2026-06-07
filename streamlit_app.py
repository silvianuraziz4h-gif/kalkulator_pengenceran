import streamlit as st
import math

# setup halaman
st.set_page_config(
    page_title="Kalkulator Kimia Analitik",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# styling custom 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

.stApp {
    background: #1a1a2e !important;
    background-image: radial-gradient(ellipse at top left, #16213e 0%, #1a1a2e 60%, #0f3460 100%) !important;
    background-attachment: fixed;
    color: #f0f0f0 !important;
}
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stMarkdown, p, label, .stSlider, .stRadio,
div[data-baseweb="checkbox"] { color: #f0f0f0 !important; }

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-baseweb="select"] div { color: #1a1a2e !important; font-weight: 500 !important; }

div[data-shaded="true"], ul[role="listbox"] li { color: #1a1a2e !important; }

button[data-baseweb="tab"] p { color: #9e9e9e !important; }
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #e8a045 !important;
    font-weight: 700 !important;
}

.badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #e8a045;
    border: 1.5px solid #e8a045;
    border-radius: 4px;
    padding: 3px 12px;
    margin-bottom: 1rem;
    background: rgba(232,160,69,0.08);
}
.main-title {
    font-size: 38px;
    font-weight: 600;
    line-height: 1.2;
    color: #fff;
    margin: 0 0 .4rem;
}
.main-title em { font-style: normal; color: #e8a045; }
.subtitle { font-size: 14px; color: #9e9e9e; line-height: 1.6; max-width: 560px; margin-bottom: 1.5rem; }

.formula-box {
    background: rgba(232,160,69,0.07);
    border: 1px solid rgba(232,160,69,0.5);
    border-radius: 8px;
    padding: 10px 16px;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: #e8a045;
    text-align: center;
    margin: 1rem 0;
}

.welcome-outer {
    max-width: 700px;
    margin: 2.5rem auto 2rem;
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}
.welcome-header {
    background: linear-gradient(135deg, #0f3460, #16213e);
    padding: 2.5rem;
    text-align: center;
    border-bottom: 2px solid #e8a045;
}
.welcome-header h1 { font-size: 36px; font-weight: 600; margin: 0; color: #fff; }
.welcome-body { padding: 2rem; text-align: center; color: #cfcfcf; }
.welcome-desc { font-size: 18px; line-height: 1.5; margin: 0 auto; max-width: 560px; }

.info-card {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 1.4rem;
    height: 100%;
    border: 1px solid rgba(255,255,255,0.07);
    border-top: 4px solid #e8a045;
}
.info-card h4 { margin-top: 0; font-size: 16px; margin-bottom: 0.6rem; color: #e8a045; }
.info-card ul { margin: 0; padding-left: 1.2rem; font-size: 14px; color: #b0b0b0; line-height: 1.7; }

.menu-card {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 1.4rem;
    min-height: 180px;
    border: 1px solid rgba(255,255,255,0.06);
    transition: background 0.2s ease, transform 0.15s ease;
}
.menu-card:hover { background: rgba(255,255,255,0.07); transform: translateY(-2px); }
.card-p1 { border-left: 4px solid #e8a045; }
.card-p2 { border-left: 4px solid #4fc3f7; }
.card-p3 { border-left: 4px solid #81c784; }
.card-p4 { border-left: 4px solid #ce93d8; }
.card-p5 { border-left: 4px solid #ef9a9a; }
.menu-icon  { font-size: 22px; margin-bottom: 0.4rem; }
.menu-title { font-size: 16px; font-weight: 600; margin: 0.2rem 0 0.4rem; color: #f0f0f0; }
.menu-desc  { font-size: 12px; color: #9e9e9e; line-height: 1.5; }

div.stButton > button {
    background: #e8a045 !important;
    color: #1a1a2e !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.55rem 1.4rem !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.02em !important;
    transition: opacity 0.15s;
}
div.stButton > button:hover { opacity: 0.88; }

.result-card {
    background: rgba(232,160,69,0.07);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-top: .75rem;
    border: 1px solid rgba(232,160,69,0.3);
}
.result-label {
    font-size: 10px;
    font-family: 'Space Mono', monospace;
    text-transform: uppercase;
    letter-spacing: .1em;
    margin: 0 0 4px;
    color: #9e9e9e;
}
.result-value {
    font-size: 24px;
    font-weight: 600;
    margin: 0;
    font-family: 'Space Mono', monospace;
    color: #e8a045;
}

div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"],
div[data-testid="stTextInput"],
div[data-testid="stTextArea"] {
    background-color: rgba(255,255,255,0.04) !important;
    border-radius: 6px !important;
}
input, select, textarea { color: white !important; }
</style>
""", unsafe_allow_html=True)


# start
if 'menu_aktif' not in st.session_state:
    st.session_state.menu_aktif = "Start"

# satuan konsentrasi
SATUAN_KONSENTRASI = ["Molaritas (M)", "% massa/volume (% m/v)", "ppm (mg/L)", "ppb (µg/L)", "mg/mL", "Molalitas (m)"]


# fungsi langkah hitung
def tampilkan_kotak(judul, konten_html):
    return f"""
    <div style="background:rgba(255,255,255,0.04); padding:20px; border-radius:10px;
                border:1px dashed rgba(232,160,69,0.4); font-family:'Courier New',monospace; margin-top:15px;">
        <p style="margin:0 0 12px 0; color:#e8a045; font-weight:600; font-size:13px;">📋 {judul}</p>
        <div style="font-size:13px; color:#cfcfcf; line-height:1.7; padding-left:5px;">
            {konten_html}
        </div>
    </div>
    """

def buat_baris(teks):
    return f"<p style='margin:0 0 8px 0;'>{teks}</p>"

# tampilan hasil
def tampilkan_hasil(nama_variabel, angka, satuan=""):
    sat_html = f'<span style="font-size:16px; color:#e8a045;">{satuan}</span>' if satuan else ""
    st.markdown(
        f'<div class="result-card">'
        f'<p class="result-label">{nama_variabel}</p>'
        f'<p class="result-value">{angka} {sat_html}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


# =============================================================
# HALAMAN START
# =============================================================
if st.session_state.menu_aktif == "Start":
    st.markdown("""
    <div class="welcome-outer">
        <div class="welcome-header"><h1>Selamat Datang👋</h1></div>
        <div class="welcome-body">
            <p class="welcome-desc" style="margin-bottom: 25px;">Aplikasi Kalkulator Kimia Analitik Kuantitatif</p>

            <img width="1024" height="1024" alt="Image" src="https://github.com/user-attachments/assets/33c8c3d4-cac9-482f-883d-0bf8a00563e3" />

        </div> 
    </div>
    """, unsafe_allow_html=True)

    _, col_tengah, _ = st.columns([1.2, 1, 1.2])
    with col_tengah:
        if st.button("Masuk ke Aplikasi →", key="btn_start", use_container_width=True):
            st.session_state.menu_aktif = "Dashboard"
            st.rerun()

    st.write("<br><br>", unsafe_allow_html=True)
    kol_kiri, kol_kanan = st.columns(2)
    with kol_kiri:
        st.markdown("""
        <div class="info-card">
            <h4>🎯 Tujuan Aplikasi</h4>
            <ul>
                <li>Menyediakan platform hitung laboratorium yang mudah dipahami.</li>
                <li>Mengecek kekeliruan pengerjaan angka desimal berkat otomasi kalkulasi analitis.</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with kol_kanan:
        st.markdown("""
        <div class="info-card">
            <h4>✨ Manfaat Aplikasi</h4>
            <ul>
                <li><b>Cepat & Efisien:</b> Memproses rumus C₁V₁=C₂V₂ dan stoikiometri dalam hitungan detik.</li>
                <li><b>Transparan:</b> Dilengkapi langkah penyelesaian lengkap dan hitung galat SD/RSD.</li>
            </ul>
        </div>""", unsafe_allow_html=True)


# =============================================================
# DASHBOARD 
# =============================================================
elif st.session_state.menu_aktif == "Dashboard":
    st.markdown('<div class="badge">🧪 Kimia Analitik</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 class="main-title">Kalkulator <em>Analisis</em> Kuantitatif</h1>
    <p class="subtitle">Pilih salah satu modul kalkulator di bawah ini untuk memulai:</p>
    """, unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)

    # modul
    daftar_modul = [
        ("col1", "card-p1", "💧", "Pengenceran Larutan",
         "Kalkulator pengenceran tunggal, serial/bertingkat, dan penentuan faktor pengenceran sampel.",
         "Pengenceran", "btn_m1"),
        ("col2", "card-p2", "🔄", "Konsentrasi & Stoikiometri",
         "Konversi antar satuan kimia (M, %, ppm, ppb) dan hitung stoikiometri reaksi mol.",
         "Stoikiometri", "btn_m2"),
        ("col3", "card-p3", "🌈", "Kesetimbangan & pH",
         "Prediksi pH sistem asam-basa kuat/lemah dan perhitungan Ka/Kb tetapan larutan.",
         "pH", "btn_m3"),
    ]
    for nama_col, css_card, ikon, judul, deskripsi, halaman, kunci_btn in daftar_modul:
        with eval(nama_col):
            st.markdown(
                f'<div class="menu-card {css_card}">'
                f'<div class="menu-icon">{ikon}</div>'
                f'<div class="menu-title">{judul}</div>'
                f'<div class="menu-desc">{deskripsi}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button(f"Buka Modul →", key=kunci_btn, use_container_width=True):
                st.session_state.menu_aktif = halaman
                st.rerun()

    st.write("")
    col4, col5, _ = st.columns(3)
    modul_baris2 = [
        (col4, "card-p4", "🧪", "Larutan Buffer",
         "Desain sistem penyangga menggunakan persamaan Henderson-Hasselbalch.",
         "Buffer", "btn_m4"),
        (col5, "card-p5", "📊", "Galat & Propagasi",
         "Hitung ketidakpastian, deviasi standar (SD), dan nilai RSD data pengukuran.",
         "Galat", "btn_m5"),
    ]
    for kolom, css_card, ikon, judul, deskripsi, halaman, kunci_btn in modul_baris2:
        with kolom:
            st.markdown(
                f'<div class="menu-card {css_card}">'
                f'<div class="menu-icon">{ikon}</div>'
                f'<div class="menu-title">{judul}</div>'
                f'<div class="menu-desc">{deskripsi}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button("Buka Modul →", key=kunci_btn, use_container_width=True):
                st.session_state.menu_aktif = halaman
                st.rerun()


# =============================================================
# MODUL-MODUL 
# =============================================================
else:
    if st.button("← Kembali ke Menu Utama", key="btn_back"):
        st.session_state.menu_aktif = "Dashboard"
        st.rerun()
    st.divider()

    # ----------------------------------------------------------
    # PENGENCERAN
    # ----------------------------------------------------------
    if st.session_state.menu_aktif == "Pengenceran":
        st.markdown("### 💧 Pengenceran Larutan")
        tab_cv, tab_serial, tab_fp = st.tabs(["C₁V₁ = C₂V₂", "Serial / Bertingkat", "Faktor Pengenceran"])

        with tab_cv:
            st.markdown('<div class="formula-box">C₁ × V₁ = C₂ × V₂</div>', unsafe_allow_html=True)
            yang_dicari = st.selectbox("Variabel yang dicari:", [
                "C₂ — Konsentrasi akhir", "V₂ — Volume akhir",
                "C₁ — Konsentrasi awal",  "V₁ — Volume awal"
            ], key="cari_cv")
            satuan = st.selectbox("Satuan konsentrasi:", ["M", "mM", "µM", "mg/mL", "ppm", "ppb"], key="satuan_cv")
            col1, col2 = st.columns(2)

            if yang_dicari == "C₂ — Konsentrasi akhir":
                with col1:
                    c1 = st.number_input("C₁", 0.0, value=1.0, format="%.5f", key="c1_c2")
                    v1 = st.number_input("V₁ (mL)", 0.0, value=10.0, format="%.3f", key="v1_c2")
                with col2:
                    v2 = st.number_input("V₂ (mL)", 1e-9, value=100.0, format="%.3f", key="v2_c2")
                jawaban = (c1 * v1) / v2
                tampilkan_hasil("C₂ — Konsentrasi akhir", f"{jawaban:.6g}", satuan)
                st.markdown(tampilkan_kotak("Penyelesaian (C₂ = C₁V₁ / V₂)",
                    buat_baris(f"C₂ = ({c1} × {v1}) / {v2}") +
                    buat_baris(f"C₂ = <b>{jawaban:.6g} {satuan}</b>")
                ), unsafe_allow_html=True)

            elif yang_dicari == "V₂ — Volume akhir":
                with col1:
                    c1 = st.number_input("C₁", 0.0, value=1.0, format="%.5f", key="c1_v2")
                    v1 = st.number_input("V₁ (mL)", 0.0, value=10.0, format="%.3f", key="v1_v2")
                with col2:
                    c2 = st.number_input("C₂", 1e-9, value=0.1, format="%.5f", key="c2_v2")
                jawaban = (c1 * v1) / c2
                tampilkan_hasil("V₂ — Volume akhir", f"{jawaban:.5g}", "mL")
                st.markdown(tampilkan_kotak("Penyelesaian (V₂ = C₁V₁ / C₂)",
                    buat_baris(f"V₂ = ({c1} × {v1}) / {c2}") +
                    buat_baris(f"V₂ = <b>{jawaban:.5g} mL</b>")
                ), unsafe_allow_html=True)

            elif yang_dicari == "C₁ — Konsentrasi awal":
                with col1:
                    v1 = st.number_input("V₁ (mL)", 1e-9, value=10.0, format="%.3f", key="v1_c1")
                    c2 = st.number_input("C₂", 0.0, value=0.1, format="%.5f", key="c2_c1")
                with col2:
                    v2 = st.number_input("V₂ (mL)", 1e-9, value=100.0, format="%.3f", key="v2_c1")
                jawaban = (c2 * v2) / v1
                tampilkan_hasil("C₁ — Konsentrasi awal", f"{jawaban:.6g}", satuan)
                st.markdown(tampilkan_kotak("Penyelesaian (C₁ = C₂V₂ / V₁)",
                    buat_baris(f"C₁ = ({c2} × {v2}) / {v1}") +
                    buat_baris(f"C₁ = <b>{jawaban:.6g} {satuan}</b>")
                ), unsafe_allow_html=True)

            else:  # V1
                with col1:
                    c1 = st.number_input("C₁", 1e-9, value=1.0, format="%.5f", key="c1_v1")
                    c2 = st.number_input("C₂", 0.0, value=0.1, format="%.5f", key="c2_v1")
                with col2:
                    v2 = st.number_input("V₂ (mL)", 1e-9, value=100.0, format="%.3f", key="v2_v1")
                jawaban = (c2 * v2) / c1
                tampilkan_hasil("V₁ — Volume awal", f"{jawaban:.5g}", "mL")
                st.markdown(tampilkan_kotak("Penyelesaian (V₁ = C₂V₂ / C₁)",
                    buat_baris(f"V₁ = ({c2} × {v2}) / {c1}") +
                    buat_baris(f"V₁ = <b>{jawaban:.5g} mL</b>")
                ), unsafe_allow_html=True)

        with tab_serial:
            n_tahap = st.slider("Jumlah tahap pengenceran:", 2, 6, 3, key="n_serial")
            c_awal = st.number_input("Konsentrasi awal C₀ (M)", 0.0, value=1.0, format="%.5f", key="c0_ser")

            c_skrg = c_awal
            langkah_html = buat_baris(f"C₀ = {c_awal} M")

            for i in range(n_tahap):
                kol_a, kol_b = st.columns(2)
                with kol_a:
                    v_ambil = st.number_input(f"V ambil tahap {i+1} (mL)", 0.001, value=1.0, key=f"va_{i}")
                with kol_b:
                    v_total = st.number_input(f"V total tahap {i+1} (mL)", 0.001, value=10.0, key=f"vt_{i}")
                fp_tahap = v_ambil / v_total
                c_skrg = c_skrg * fp_tahap
                langkah_html += buat_baris(
                    f"Tahap {i+1}: {v_ambil} mL → {v_total} mL, FP = {fp_tahap:.4f}, C = <b>{c_skrg:.4e} M</b>"
                )

            tampilkan_hasil("Konsentrasi Akhir (serial)", f"{c_skrg:.4e}", "M")
            st.markdown(tampilkan_kotak("Penyelesaian (Pengenceran Serial)", langkah_html), unsafe_allow_html=True)

        with tab_fp:
            kol_a, kol_b = st.columns(2)
            with kol_a:
                va_fp = st.number_input("Volume sampel (mL)", 0.001, value=1.0, key="fp_va")
                ca_fp = st.number_input("Konsentrasi awal (opsional)", 0.0, value=1.0, format="%.5f", key="fp_ca")
            with kol_b:
                vb_fp = st.number_input("Volume akhir (mL)", 0.001, value=100.0, key="fp_vb")
            fp = vb_fp / va_fp
            tampilkan_hasil("Faktor Pengenceran", f"1 : {fp:.4f}")
            tampilkan_hasil("Konsentrasi Akhir", f"{ca_fp / fp:.5g}")
            st.markdown(tampilkan_kotak("Penyelesaian (Faktor Pengenceran)",
                buat_baris(f"FP = {vb_fp} / {va_fp} = <b>{fp:.4f}</b>") +
                buat_baris(f"C akhir = {ca_fp} / {fp:.4f} = <b>{ca_fp / fp:.5g}</b>")
            ), unsafe_allow_html=True)

    # ----------------------------------------------------------
    # STOIKIOMETRI
    # ----------------------------------------------------------
    elif st.session_state.menu_aktif == "Stoikiometri":
        st.markdown("### 🔄 Satuan Konsentrasi & Stoikiometri")
        tab_konv, tab_mol, tab_reaksi = st.tabs(["🔄 Konversi Satuan", "⚖️ Mol & Massa", "🧮 Stoikiometri Reaksi"])

        with tab_konv:
            col1, col2 = st.columns(2)
            with col1:
                satuan_dari = st.selectbox("Dari satuan:", SATUAN_KONSENTRASI, index=0, key="k_dari")
                nilai_input  = st.number_input("Nilai", 0.0, value=1.0, format="%.6f", key="k_val")
                mr_zat       = st.number_input("Mr zat (g/mol)", 0.001, value=58.44, key="k_mr")
            with col2:
                satuan_ke = st.selectbox("Ke satuan:", SATUAN_KONSENTRASI, index=2, key="k_ke")
                densitas  = st.number_input("Densitas ρ (g/mL)", 0.001, value=1.0, key="k_rho")

            if satuan_dari == satuan_ke:
                st.warning("Pilih satuan yang berbeda.")
            else:
                # konversi dua langkah: satuan asal → mg/L → satuan target
                ke_mgL = {
                    "Molaritas (M)":            lambda v: v * mr_zat * 1000,
                    "% massa/volume (% m/v)":   lambda v: v * 10000,
                    "ppm (mg/L)":               lambda v: v,
                    "ppb (µg/L)":               lambda v: v / 1000,
                    "mg/mL":                    lambda v: v * 1000,
                    "Molalitas (m)":            lambda v: v * mr_zat * densitas * 1000,
                }
                dari_mgL = {
                    "Molaritas (M)":            lambda v: v / (mr_zat * 1000),
                    "% massa/volume (% m/v)":   lambda v: v / 10000,
                    "ppm (mg/L)":               lambda v: v,
                    "ppb (µg/L)":               lambda v: v * 1000,
                    "mg/mL":                    lambda v: v / 1000,
                    "Molalitas (m)":            lambda v: v / (mr_zat * densitas * 1000),
                }
                nilai_mgL = ke_mgL[satuan_dari](nilai_input)
                nilai_target = dari_mgL[satuan_ke](nilai_mgL)
                tampilkan_hasil("Hasil Konversi", f"{nilai_target:.6g}", satuan_ke)
                st.markdown(tampilkan_kotak("Penyelesaian (via basis mg/L)",
                    buat_baris(f"'{satuan_dari}' → mg/L: <b>{nilai_mgL:.4e} mg/L</b>") +
                    buat_baris(f"mg/L → '{satuan_ke}': <b>{nilai_target:.6g} {satuan_ke}</b>") +
                    buat_baris(f"<span style='color:#9e9e9e;font-size:11px'>Mr = {mr_zat} g/mol | ρ = {densitas} g/mL</span>")
                ), unsafe_allow_html=True)

        with tab_mol:
            pilihan = st.selectbox("Cari:", [
                "Mol (n) dari massa & Mr", "Mol (n) dari M & V",
                "Massa (g) dari n & Mr",   "Molaritas (M) dari n & V",
                "Volume (mL) dari n & M"
            ], key="pilihan_mol")
            col1, col2 = st.columns(2)

            if "massa & Mr" in pilihan:
                with col1: massa = st.number_input("Massa (gram)", 0.0, value=5.85, format="%.4f", key="mol_m")
                with col2: mr    = st.number_input("Mr (g/mol)", 0.001, value=58.44, key="mol_mr")
                n = massa / mr
                tampilkan_hasil("Mol (n)", f"{n:.5g}", "mol")
                st.markdown(tampilkan_kotak("n = gram / Mr",
                    buat_baris(f"n = {massa} / {mr} = <b>{n:.5g} mol</b>")
                ), unsafe_allow_html=True)

            elif "M & V" in pilihan:
                with col1: M_val = st.number_input("Molaritas (M)", 0.0, value=1.0, key="mol_M")
                with col2: V_val = st.number_input("Volume (mL)", 0.0, value=100.0, key="mol_V")
                n = M_val * (V_val / 1000)
                tampilkan_hasil("Mol (n)", f"{n:.5g}", "mol")
                st.markdown(tampilkan_kotak("n = M × (V/1000)",
                    buat_baris(f"n = {M_val} × ({V_val}/1000) = <b>{n:.5g} mol</b>")
                ), unsafe_allow_html=True)

            elif "Massa" in pilihan:
                with col1: n_input = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_n_m")
                with col2: mr = st.number_input("Mr (g/mol)", 0.001, value=58.44, key="mol_mr2")
                gram = n_input * mr
                tampilkan_hasil("Massa (m)", f"{gram:.5g}", "gram")
                st.markdown(tampilkan_kotak("gram = n × Mr",
                    buat_baris(f"gram = {n_input} × {mr} = <b>{gram:.5g} gram</b>")
                ), unsafe_allow_html=True)

            elif "Molaritas" in pilihan:
                with col1: n_input = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_n_M")
                with col2: V_val = st.number_input("Volume (mL)", 0.001, value=100.0, key="mol_V2")
                M_hsl = n_input / (V_val / 1000)
                tampilkan_hasil("Molaritas (M)", f"{M_hsl:.5g}", "mol/L")
                st.markdown(tampilkan_kotak("M = n / (V/1000)",
                    buat_baris(f"M = {n_input} / ({V_val}/1000) = <b>{M_hsl:.5g} M</b>")
                ), unsafe_allow_html=True)

            else:  # Volume
                with col1: n_input = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_n_V")
                with col2: M_val = st.number_input("Molaritas (M)", 0.001, value=1.0, key="mol_M2")
                V_hsl = (n_input / M_val) * 1000
                tampilkan_hasil("Volume (V)", f"{V_hsl:.5g}", "mL")
                st.markdown(tampilkan_kotak("V (mL) = (n/M) × 1000",
                    buat_baris(f"V = ({n_input}/{M_val}) × 1000 = <b>{V_hsl:.5g} mL</b>")
                ), unsafe_allow_html=True)

        with tab_reaksi:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                kA = st.number_input("Koef A", 1, value=1, key="kA")
                nA = st.text_input("Nama A", "HCl", key="nA")
                mA = st.number_input("Mr A", 0.001, value=36.46, key="mA")
            with col2:
                kB = st.number_input("Koef B", 1, value=1, key="kB")
                nB = st.text_input("Nama B", "NaOH", key="nB")
                mB = st.number_input("Mr B", 0.001, value=40.00, key="mB")
            with col3:
                kC = st.number_input("Koef C", 1, value=1, key="kC")
                nC = st.text_input("Nama C", "NaCl", key="nC")
                mC = st.number_input("Mr C", 0.001, value=58.44, key="mC")
            with col4:
                kD = st.number_input("Koef D", 1, value=1, key="kD")
                nD = st.text_input("Nama D", "H₂O", key="nD")
                mD = st.number_input("Mr D", 0.001, value=18.02, key="mD")

            st.info(f"**Reaksi:** {kA} {nA} + {kB} {nB} → {kC} {nC} + {kD} {nD}")
            reaktan_pembatas = st.selectbox("Reaktan pembatas:", [nA, nB], key="reaktan")
            mol_pembatas = st.number_input("Mol Reaktan Pembatas", 0.0, value=0.1, key="n_pem")

            k_ref = kA if reaktan_pembatas == nA else kB
            mol_C = mol_pembatas * (kC / k_ref)

            tampilkan_hasil(f"Hasil {nC}", f"{mol_C:.5g} mol ({mol_C * mC:.5g} g)")
            st.markdown(tampilkan_kotak("Penyelesaian (perbandingan koefisien)",
                buat_baris(f"Mol {nC} = ({kC}/{k_ref}) × {mol_pembatas} = <b>{mol_C:.5g} mol</b>") +
                buat_baris(f"Massa {nC} = {mol_C:.5g} × {mC} = <b>{mol_C * mC:.5g} gram</b>")
            ), unsafe_allow_html=True)

    # ----------------------------------------------------------
    # pH & KESETIMBANGAN
    # ----------------------------------------------------------
    elif st.session_state.menu_aktif == "pH":
        st.markdown("### 🌈 Kesetimbangan & Perubahan pH")
        tab_asam, tab_basa, tab_ka, tab_dilusi = st.tabs([
            "🔴 pH Asam", "🔵 pH Basa", "🔬 Hitung Ka/Kb", "📉 ΔpH Pengenceran"
        ])

        with tab_asam:
            tipe_asam = st.radio("Jenis asam:", ["Asam Kuat", "Asam Lemah"], horizontal=True, key="jenis_asam")
            C = st.number_input("Konsentrasi C (M)", 1e-14, value=0.1, key="C_asam")
            if tipe_asam == "Asam Kuat":
                pH = -math.log10(max(C, 1e-14))
                tampilkan_hasil("pH Larutan", f"{pH:.4f}")
                st.markdown(tampilkan_kotak("pH = -log[H⁺]",
                    buat_baris(f"[H⁺] = {C} M") +
                    buat_baris(f"pH = -log({C}) = <b>{pH:.4f}</b>")
                ), unsafe_allow_html=True)
            else:
                Ka = st.number_input("Ka", 1e-20, value=1.8e-5, key="Ka_asam")
                h  = math.sqrt(Ka * C)
                pH = -math.log10(h)
                tampilkan_hasil("pH Larutan", f"{pH:.4f}")
                st.markdown(tampilkan_kotak("pH Asam Lemah: [H⁺] = √(Ka × C)",
                    buat_baris(f"[H⁺] = √({Ka} × {C}) = {h:.4e} M") +
                    buat_baris(f"pH = -log({h:.4e}) = <b>{pH:.4f}</b>")
                ), unsafe_allow_html=True)

        with tab_basa:
            tipe_basa = st.radio("Jenis basa:", ["Basa Kuat", "Basa Lemah"], horizontal=True, key="jenis_basa")
            C = st.number_input("Konsentrasi C (M)", 1e-14, value=0.1, key="C_basa")
            if tipe_basa == "Basa Kuat":
                pH = 14 + math.log10(C)
                tampilkan_hasil("pH Larutan", f"{pH:.4f}")
                st.markdown(tampilkan_kotak("pH = 14 - pOH",
                    buat_baris(f"pOH = -log({C}) = {-math.log10(C):.4f}") +
                    buat_baris(f"pH = 14 - pOH = <b>{pH:.4f}</b>")
                ), unsafe_allow_html=True)
            else:
                Kb = st.number_input("Kb", 1e-20, value=1.8e-5, key="Kb_basa")
                oh = math.sqrt(Kb * C)
                pH = 14 + math.log10(oh)
                tampilkan_hasil("pH Larutan", f"{pH:.4f}")
                st.markdown(tampilkan_kotak("pH Basa Lemah: [OH⁻] = √(Kb × C)",
                    buat_baris(f"[OH⁻] = √({Kb} × {C}) = {oh:.4e} M") +
                    buat_baris(f"pOH = -log({oh:.4e}) = {-math.log10(oh):.4f}") +
                    buat_baris(f"pH = 14 - pOH = <b>{pH:.4f}</b>")
                ), unsafe_allow_html=True)

        with tab_ka:
            C  = st.number_input("Konsentrasi C (M)", 1e-10, value=0.1, key="C_ka")
            pH = st.number_input("pH terukur", 0.0, 14.0, value=2.87, key="pH_ka")
            H  = 10 ** (-pH)
            if C > H:
                Ka = H**2 / (C - H)
                tampilkan_hasil("Ka Prediksi", f"{Ka:.4e}")
                st.markdown(tampilkan_kotak("Ka = [H⁺]² / (C - [H⁺])",
                    buat_baris(f"[H⁺] = 10^(-{pH}) = {H:.4e} M") +
                    buat_baris(f"Ka = ({H:.4e})² / ({C} - {H:.4e}) = <b>{Ka:.4e}</b>")
                ), unsafe_allow_html=True)

        with tab_dilusi:
            tipe_dil = st.radio("Jenis larutan:", ["Asam Kuat", "Asam Lemah", "Basa Kuat", "Basa Lemah"],
                             horizontal=True, key="jenis_dilusi")
            C1 = st.number_input("C₁ (M)", 1e-14, value=0.1, key="C1_dil")
            V1 = st.number_input("V₁ (mL)", 0.001, value=10.0, key="V1_dil")
            V2 = st.number_input("V₂ (mL)", 0.001, value=100.0, key="V2_dil")
            K_val = st.number_input("Ka / Kb", 1e-20, value=1.8e-5, key="K_dil") if "Lemah" in tipe_dil else None

            def hitung_pH_larutan(konsentrasi, tipe, K):
                c = max(konsentrasi, 1e-14)
                if tipe == "Asam Kuat":   return -math.log10(c)
                if tipe == "Asam Lemah":  return -math.log10(math.sqrt(K * c))
                if tipe == "Basa Kuat":   return 14 + math.log10(c)
                if tipe == "Basa Lemah":  return 14 + math.log10(math.sqrt(K * c))

            C2  = C1 * V1 / V2
            pH1 = hitung_pH_larutan(C1, tipe_dil, K_val)
            pH2 = hitung_pH_larutan(C2, tipe_dil, K_val)
            delta_pH = abs(pH2 - pH1)
            tampilkan_hasil("pH Akhir", f"{pH2:.4f}", f"(Awal: {pH1:.4f})")
            st.markdown(tampilkan_kotak("Penyelesaian (Efek Dilusi terhadap pH)",
                buat_baris(f"C₂ = ({C1} × {V1}) / {V2} = <b>{C2:.4e} M</b>") +
                buat_baris(f"pH₁ (C₁) = <b>{pH1:.4f}</b>") +
                buat_baris(f"pH₂ (C₂) = <b>{pH2:.4f}</b>") +
                buat_baris(f"ΔpH = <b>{delta_pH:.4f}</b>")
            ), unsafe_allow_html=True)

    # ----------------------------------------------------------
    # BUFFER
    # ----------------------------------------------------------
    elif st.session_state.menu_aktif == "Buffer":
        st.markdown("### 🧪 Pembuatan Larutan Buffer")
        tab_ph, tab_rasio, tab_beta = st.tabs([
            "🧮 Hitung pH Buffer", "⚖️ Hitung Rasio [A⁻]/[HA]", "📊 Kapasitas Buffer (β)"
        ])

        with tab_ph:
            pKa = st.number_input("pKa asam", 0.0, 14.0, value=4.74, key="pka_buf")
            ab  = st.number_input("[A⁻] Basa Konjugat (M)", 0.0001, value=0.1, key="ab_buf")
            ha  = st.number_input("[HA] Asam (M)", 0.0001, value=0.1, key="ha_buf")
            pH_buf = pKa + math.log10(ab / ha)
            tampilkan_hasil("pH Buffer", f"{pH_buf:.4f}")
            st.markdown(tampilkan_kotak("Henderson-Hasselbalch: pH = pKa + log([A⁻]/[HA])",
                buat_baris(f"pH = {pKa} + log({ab}/{ha})") +
                buat_baris(f"pH = {pKa} + {math.log10(ab/ha):.4f} = <b>{pH_buf:.4f}</b>")
            ), unsafe_allow_html=True)

        with tab_rasio:
            pH_target = st.number_input("pH target", 0.0, 14.0, value=5.0, key="pH_rasio")
            pKa_r     = st.number_input("pKa asam", 0.0, 14.0, value=4.74, key="pka_rasio")
            C_total   = st.number_input("Konsentrasi total (M)", 0.001, value=0.2, key="Ctot_rasio")
            rasio = 10 ** (pH_target - pKa_r)
            konj  = C_total * rasio / (1 + rasio)
            asam  = C_total / (1 + rasio)
            tampilkan_hasil("Rasio [A⁻]/[HA]", f"{rasio:.5f}", f"([A⁻]={konj:.4f}M)")
            st.markdown(tampilkan_kotak("Rasio = 10^(pH - pKa)",
                buat_baris(f"[A⁻]/[HA] = 10^({pH_target} - {pKa_r}) = <b>{rasio:.5f}</b>") +
                buat_baris(f"[A⁻] = ({rasio:.5f} / (1+{rasio:.5f})) × {C_total} = <b>{konj:.4f} M</b>") +
                buat_baris(f"[HA] = {C_total} - {konj:.4f} = <b>{asam:.4f} M</b>")
            ), unsafe_allow_html=True)

        with tab_beta:
            C_tot = st.number_input("Konsentrasi total (M)", 0.0001, value=0.1, key="Ctot_beta")
            Ka_b  = st.number_input("Ka", 1e-20, value=1.8e-5, key="Ka_beta")
            pH_b  = st.number_input("pH larutan", 0.0, 14.0, value=4.74, key="pH_beta")
            H_b   = 10 ** (-pH_b)
            beta  = 2.303 * C_tot * (Ka_b * H_b) / (Ka_b + H_b)**2
            tampilkan_hasil("Kapasitas Buffer (β)", f"{beta:.4e}")
            st.markdown(tampilkan_kotak("Van Slyke: β = 2.303 × C × Ka[H⁺] / (Ka+[H⁺])²",
                buat_baris(f"[H⁺] = 10^(-{pH_b}) = {H_b:.4e} M") +
                buat_baris(f"β = 2.303 × {C_tot} × ({Ka_b:.2e} × {H_b:.2e}) / ({Ka_b:.2e} + {H_b:.2e})²") +
                buat_baris(f"β = <b>{beta:.4e}</b>")
            ), unsafe_allow_html=True)

    # ----------------------------------------------------------
    # GALAT & PROPAGASI ERROR
    # ----------------------------------------------------------
    elif st.session_state.menu_aktif == "Galat":
        st.markdown("### 📊 Galat & Propagasi Error")
        tab_ga, tab_prop, tab_stat = st.tabs([
            "📏 Galat Absolut & Relatif", "⚡ Propagasi Error", "📊 Statistik (SD & RSD)"
        ])

        with tab_ga:
            x_ukur  = st.number_input("Nilai terukur", value=9.87, key="x_ukur")
            x_benar = st.number_input("Nilai benar / referensi", value=10.00, key="x_benar")
            g_abs = abs(x_ukur - x_benar)
            g_rel = (g_abs / x_benar) * 100
            tampilkan_hasil("Galat Absolut", f"{g_abs:.5g}")
            st.markdown(tampilkan_kotak("Galat Absolut & Relatif",
                buat_baris(f"Galat Absolut = |{x_ukur} - {x_benar}| = <b>{g_abs:.5g}</b>") +
                buat_baris(f"Galat Relatif = ({g_abs:.5g} / {x_benar}) × 100 = <b>{g_rel:.3f}%</b>")
            ), unsafe_allow_html=True)

        with tab_prop:
            jenis_op = st.selectbox("Operasi:", [
                "Penjumlahan / Pengurangan (x ± y)",
                "Perkalian / Pembagian (x × y atau x/y)"
            ], key="op_prop")
            x_val  = st.number_input("Nilai x", value=10.0, key="xv")
            dx_val = st.number_input("δx", value=0.05, key="dxv")
            y_val  = st.number_input("Nilai y", value=5.0, key="yv")
            dy_val = st.number_input("δy", value=0.03, key="dyv")

            if "Penjumlahan" in jenis_op:
                unc = math.sqrt(dx_val**2 + dy_val**2)
                tampilkan_hasil("Ketidakpastian Akhir", f"± {unc:.5g}")
                st.markdown(tampilkan_kotak("δz = √(δx² + δy²)",
                    buat_baris(f"δz = √({dx_val}² + {dy_val}²) = √({dx_val**2:.5f} + {dy_val**2:.5f})") +
                    buat_baris(f"δz = <b>± {unc:.5g}</b>")
                ), unsafe_allow_html=True)
            else:
                z_val = x_val * y_val
                unc   = z_val * math.sqrt((dx_val/x_val)**2 + (dy_val/y_val)**2)
                tampilkan_hasil("Ketidakpastian Akhir", f"± {unc:.5g}")
                st.markdown(tampilkan_kotak("δz/z = √((δx/x)² + (δy/y)²)",
                    buat_baris(f"z = {x_val} × {y_val} = {z_val}") +
                    buat_baris(f"δz = {z_val} × √(({dx_val}/{x_val})² + ({dy_val}/{y_val})²)") +
                    buat_baris(f"δz = <b>± {unc:.5g}</b>")
                ), unsafe_allow_html=True)

        with tab_stat:
            teks_data = st.text_area("Data pengukuran (pisahkan dengan koma):",
                               value="9.87, 9.92, 9.85, 9.90, 9.88", key="data_stat")
            # parsing manual - cukup pakai split saja
            angka_data = []
            for tok in teks_data.split(','):
                tok = tok.strip()
                if tok:
                    try:
                        angka_data.append(float(tok))
                    except ValueError:
                        pass

            if len(angka_data) >= 2:
                rata2 = sum(angka_data) / len(angka_data)
                sd    = math.sqrt(sum((x - rata2)**2 for x in angka_data) / (len(angka_data) - 1))
                rsd   = (sd / rata2) * 100
                tampilkan_hasil("Rata-rata ± SD", f"{rata2:.4g} ± {sd:.4g}", f"(RSD: {rsd:.3f}%)")
                st.markdown(tampilkan_kotak("Statistik Deskriptif",
                    buat_baris(f"n = {len(angka_data)} data") +
                    buat_baris(f"Rata-rata (μ) = Σx / n = <b>{rata2:.4g}</b>") +
                    buat_baris(f"SD = √(Σ(xᵢ-μ)² / (n-1)) = <b>{sd:.4g}</b>") +
                    buat_baris(f"RSD = (SD/μ) × 100% = <b>{rsd:.3f}%</b>")
                ), unsafe_allow_html=True)


st.divider()
st.markdown(
    '<p style="text-align:center; font-size:12px; color:#9e9e9e;">⚗️ Kalkulator Analisis Kuantitatif · Kimia Analitik</p>',
    unsafe_allow_html=True
)

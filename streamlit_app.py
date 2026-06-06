import streamlit as st
import math

# 1. PENGATURAN HALAMAN
st.set_page_config(
    page_title="Kalkulator Analisis Kuantitatif",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. GAYA CSS CUSTOM
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { 
    font-family: 'DM Sans', sans-serif; 
}
.main > div { 
    padding-top: 1.5rem; 
    padding-bottom: 3rem; 
}
.badge { 
    display:inline-block; font-family:'DM Mono',monospace; font-size:11px; font-weight:500;
    letter-spacing:.08em; text-transform:uppercase; color:#5F5E5A; border:1px solid #D3D1C7;
    border-radius:999px; padding:4px 14px; margin-bottom:1rem; 
}
.main-title { 
    font-family:'DM Serif Display',serif; font-size:40px; line-height:1.15; color:#1a1a1a; margin:0 0 .5rem; 
}
.main-title em { 
    font-style:italic; color:#1D9E75; 
}
.subtitle { 
    font-size:15px; color:#6b6b6b; line-height:1.6; max-width:600px; margin-bottom:1.5rem; 
}
.formula-box { 
    background:#f7f9fc; border:1px solid #e0eaf5; border-radius:10px; padding:12px 16px;
    font-family:'DM Mono',monospace; font-size:13px; color:#185FA5; text-align:center; margin:1rem 0; 
}

/* Style untuk Start Page & Welcome Screen */
.welcome-container {
    text-align: center;
    padding: 3rem 2rem 1.5rem;
    background: #fafbfc;
    border: 1px solid #e8e8e8;
    border-radius: 20px;
    margin-top: 1rem;
}
.welcome-icon { font-size: 60px; margin-bottom: 0.5rem; }
.welcome-title { font-family: 'DM Serif Display', serif; font-size: 46px; color: #1a1a1a; margin-bottom: 0.5rem; }
.welcome-desc { font-size: 16px; color: #555; max-width: 700px; margin: 0 auto 1rem; line-height: 1.6; }

/* Info Box untuk Tujuan & Manfaat di Start Page */
.info-block {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: left;
    height: 100%;
}
.info-block h4 {
    margin-top: 0;
    color: #1D9E75;
    font-size: 18px;
    margin-bottom: 0.5rem;
}
.info-block ul {
    margin: 0;
    padding-left: 1.2rem;
    font-size: 14px;
    color: #555;
    line-height: 1.5;
}

/* Style untuk Kartu Menu Utama */
.menu-card {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1.5rem;
    height: 100%;
    transition: all 0.2s ease;
}
.menu-card:hover {
    border-color: #1D9E75;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.menu-icon { font-size: 24px; margin-bottom: 0.5rem; }
.menu-num { font-family: 'DM Mono', monospace; font-size: 12px; color: #888; }
.menu-title { font-size: 18px; font-weight: 500; margin-top: 0.25rem; margin-bottom: 0.5rem; color: #1a1a1a; }
.menu-desc { font-size: 13px; color: #666; line-height: 1.5; margin-bottom: 1rem; }

.rc-green  { background:#f0fdf7; border:1.5px solid #1D9E75; }
.rc-blue   { background:#f0f6ff; border:1.5px solid #378ADD; }
.rc-amber  { background:#fffaf0; border:1.5px solid #EF9F27; }
.rc-purple { background:#f5f4ff; border:1.5px solid #7F77DD; }
.rc-coral  { background:#fff5f2; border:1.5px solid #D85A30; }

.result-card { border-radius:12px; padding:1rem 1.4rem; margin-top:.75rem; }
.result-label { font-size:11px; font-family:'DM Mono',monospace; text-transform:uppercase; letter-spacing:.07em; margin:0 0 4px; }
.result-value { font-size:26px; font-weight:500; margin:0; font-family:'DM Mono',monospace; }
.step-box { background:#fafafa; border:1px solid #e0e0e0; border-radius:8px; padding:10px 14px; margin-top:8px; font-size:12.5px; color:#555; font-family:'DM Mono',monospace; line-height:1.9; }
.ph-bar  { height:14px; background:#eee; border-radius:7px; overflow:hidden; margin-top:6px; }
.ph-fill { height:100%; border-radius:7px; }
</style>
""", unsafe_allow_html=True)

# 3. STATE MANAGEMENT NAVIGASI
if 'menu_aktif' not in st.session_state:
    st.session_state.menu_aktif = "Start"

def pindah_ke(nama_modul):
    st.session_state.menu_aktif = nama_modul

# Fungsi helper perhitungan kalkulator
def ph_color(ph):
    if ph < 3:  return "#E24B4A"
    if ph < 6:  return "#EF9F27"
    if ph < 8:  return "#1D9E75"
    if ph < 11: return "#378ADD"
    return "#7F77DD"

def ph_bar(ph):
    pct = min(max(ph / 14 * 100, 0), 100)
    return f'<div class="ph-bar"><div class="ph-fill" style="width:{pct:.1f}%;background:{ph_color(ph)}"></div></div>'

def res(label, value, unit="", color_cls="rc-green", extra_style=""):
    return f'<div class="result-card {color_cls}" style="{extra_style}"><p class="result-label">{label}</p><p class="result-value">{value} <span style="font-size:14px">{unit}</span></p></div>'

def step(html):
    return f'<div class="step-box">{html}</div>'

def calc_ph(jenis, C, K=None):
    C = max(C, 1e-14)
    if jenis == "ak": return -math.log10(C)
    if jenis == "al": return -math.log10(math.sqrt(max(K * C, 1e-28)))
    if jenis == "bk": return 14 + math.log10(C)
    if jenis == "bl": return 14 + math.log10(math.sqrt(max(K * C, 1e-28)))

SATUAN_KONSENTRASI = ["Molaritas (M)", "% massa/volume (% m/v)", "ppm (mg/L)", "ppb (µg/L)", "mg/mL", "Molalitas (m)"]

def to_mgL(val, sat, mr, rho=1.0):
    tabel = {"Molaritas (M)": val*mr*1000, "% massa/volume (% m/v)": val*10000,
             "ppm (mg/L)": val, "ppb (µg/L)": val/1000, "mg/mL": val*1000,
             "Molalitas (m)": val*mr*rho*1000}
    return tabel.get(sat, val)

def from_mgL(mgL, sat, mr, rho=1.0):
    tabel = {"Molaritas (M)": mgL/(mr*1000), "% massa/volume (% m/v)": mgL/10000,
             "ppm (mg/L)": mgL, "ppb (µg/L)": mgL*1000, "mg/mL": mgL/1000,
             "Molalitas (m)": mgL/(mr*rho*1000)}
    return tabel.get(sat, mgL)


# ==========================================
# HALAMAN ISI KONTEN (TERGANTUNG STATE)
# ==========================================

# --- HALAMAN PEMBUKA (START PAGE) ---
if st.session_state.menu_aktif == "Start":
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-icon">⚗️</div>
        <div class="welcome-title">Selamat Datang</div>
        <p class="welcome-desc">
            Aplikasi interaktif terintegrasi untuk Laboratorium Kimia Analitik Kuantitatif.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menambahkan Tujuan & Manfaat berdampingan di halaman Start
    st.write("")
    col_tujuan, col_manfaat = st.columns(2)
    with col_tujuan:
        st.markdown("""
        <div class="info-block">
            <h4>🎯 Tujuan Aplikasi</h4>
            <ul>
                <li>Menyediakan platform komputasi kimia analitik yang cepat, presisi, dan bebas dari risiko <i>human error</i> saat kalkulasi manual.</li>
                <li>Menyederhanakan alur kerja laboratorium dari persiapan sampel hingga analisis data akhir dalam satu tempat.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_manfaat:
        st.markdown("""
        <div class="info-block">
            <h4>✨ Manfaat Aplikasi</h4>
            <ul>
                <li><b>Efisiensi Waktu:</b> Mempercepat proses pembuatan larutan kerja dan perhitungan stoikiometri reaksi secara instan.</li>
                <li><b>Akurasi Tinggi:</b> Dilengkapi dengan fitur pelacakan langkah perhitungan dan analisis perambatan galat ketidakpastian data.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    # Tombol besar di tengah halaman pembuka
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🚀 MASUK KE APLIKASI", key="btn_start", use_container_width=True):
            pindah_ke("Dashboard"); st.rerun()

# --- HALAMAN MENU UTAMA (DASHBOARD KARTU) ---
elif st.session_state.menu_aktif == "Dashboard":
    st.markdown('<div class="badge">⚗ Kimia Analitik</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 class="main-title">Kalkulator <em>Analisis</em> Kuantitatif</h1>
    <p class="subtitle">Alat perhitungan terintegrasi untuk kimia analitik. Klik pada modul di bawah untuk mulai menghitung.</p>
    """, unsafe_allow_html=True)
    
    # Menggunakan st.expander untuk informasi Tujuan & Manfaat sebelum barisan menu kalkulator
    with st.expander("📌 Lihat Informasi Tujuan & Manfaat Aplikasi", expanded=False):
        col_tuj_dash, col_man_dash = st.columns(2)
        with col_tuj_dash:
            st.markdown("##### 🎯 Tujuan")
            st.info("Membantu praktikan, laboran, dan peneliti dalam melakukan validasi perhitungan kimia analitik kuantitatif secara cepat dan akurat demi meminimalkan kesalahan preparasi sampel.")
        with col_man_dash:
            st.markdown("##### ✨ Manfaat")
            st.success("Menghemat waktu pengerjaan analisis di lab, mempermudah penentuan rasio buffer/pH, serta membantu pengolahan data statistik berbasis ketidakpastian (galat) secara otomatis.")
            
    st.divider()
    
    st.write("##### MODUL TERSEDIA — 5 TOPIK")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="menu-card">
            <div class="menu-icon">💧</div>
            <div class="menu-num">01</div>
            <div class="menu-title">Pengenceran Larutan</div>
            <div class="menu-desc">Hitung volume/konsentrasi pengenceran tunggal maupun bertingkat (C₁V₁ = C₂V₂).</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Kalkulator Pengenceran ➡️", key="btn_m1", use_container_width=True):
            pindah_ke("Pengenceran"); st.rerun()
            
    with col2:
        st.markdown("""
        <div class="menu-card">
            <div class="menu-icon">⇌</div>
            <div class="menu-num">02</div>
            <div class="menu-title">Konsentrasi & Stoikiometri</div>
            <div class="menu-desc">Konversi antar satuan konsentrasi (M, %, ppm, ppb) dan hitung stoikiometri mol.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Kalkulator Stoikiometri ➡️", key="btn_m2", use_container_width=True):
            pindah_ke("Stoikiometri"); st.rerun()

    with col3:
        st.markdown("""
        <div class="menu-card">
            <div class="menu-icon">📈</div>
            <div class="menu-num">03</div>
            <div class="menu-title">Kesetimbangan & pH</div>
            <div class="menu-desc">Prediksi asam-basa, nilai Ka/Kb, serta simulasi delta pH setelah pengenceran.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Kalkulator pH ➡️", key="btn_m3", use_container_width=True):
            pindah_ke("pH"); st.rerun()

    st.write("")
    col4, col5, _ = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="menu-card">
            <div class="menu-icon">🧪</div>
            <div class="menu-num">04</div>
            <div class="menu-title">Larutan Buffer</div>
            <div class="menu-desc">Rancang larutan penyangga asam-basa berdasarkan pH target Henderson-Hasselbalch.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Pembuat Buffer ➡️", key="btn_m4", use_container_width=True):
            pindah_ke("Buffer"); st.rerun()
            
    with col5:
        st.markdown("""
        <div class="menu-card">
            <div class="menu-icon">±</div>
            <div class="menu-num">05</div>
            <div class="menu-title">Galat & Propagasi</div>
            <div class="menu-desc">Hitung ketidakpastian galat absolut/relatif, SD, RSD, dan propagasi error matematika.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Analisis Galat ➡️", key="btn_m5", use_container_width=True):
            pindah_ke("Galat"); st.rerun()

# --- HALAMAN MODUL SELEKSI KALKULATOR ---
else:
    if st.button("⬅️ Kembali ke Menu Utama", key="btn_kembali"):
        pindah_ke("Dashboard"); st.rerun()
    st.divider()

    # MODUL 1 — PENGENCERAN
    if st.session_state.menu_aktif == "Pengenceran":
        st.markdown("### 💧 Pengenceran Larutan")
        t1a, t1b, t1c = st.tabs(["C₁V₁ = C₂V₂", "Serial / Bertingkat", "Faktor Pengenceran"])
        with t1a:
            st.markdown("""<div class="formula-box">C₁ × V₁ = C₂ × V₂</div>""", unsafe_allow_html=True)
            cari = st.selectbox("Variabel yang dicari:", ["C₂ — Konsentrasi akhir","V₂ — Volume akhir","C₁ — Konsentrasi awal","V₁ — Volume awal"], key="e_cari")
            satuan = st.selectbox("Satuan konsentrasi:", ["M","mM","µM","mg/mL","ppm","ppb"], key="e_sat")
            col1, col2 = st.columns(2)
            if cari == "C₂ — Konsentrasi akhir":
                with col1:
                    c1 = st.number_input("C₁ — Konsentrasi awal", 0.0, value=1.0, format="%.5f", key="ec1a")
                    v1 = st.number_input("V₁ — Volume awal (mL)",  0.0, value=10.0, format="%.3f", key="ev1a")
                with col2: v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, format="%.3f", key="ev2a")
                hasil = (c1*v1)/v2
                st.markdown(res("C₂ — Konsentrasi akhir", f"{hasil:.6g}", satuan, "rc-green"), unsafe_allow_html=True)
            elif cari == "V₂ — Volume akhir":
                with col1:
                    c1 = st.number_input("C₁ — Konsentrasi awal", 0.0, value=1.0, format="%.5f", key="ec1b")
                    v1 = st.number_input("V₁ — Volume awal (mL)",  0.0, value=10.0, format="%.3f", key="ev1b")
                with col2: c2 = st.number_input("C₂ — Konsentrasi akhir", 1e-9, value=0.1, format="%.5f", key="ec2b")
                hasil = (c1*v1)/c2
                st.markdown(res("V₂ — Volume akhir", f"{hasil:.5g}", "mL", "rc-green"), unsafe_allow_html=True)
            elif cari == "C₁ — Konsentrasi awal":
                with col1:
                    v1 = st.number_input("V₁ — Volume awal (mL)",  1e-9, value=10.0, format="%.3f", key="ev1c")
                    c2 = st.number_input("C₂ — Konsentrasi akhir", 0.0,  value=0.1, format="%.5f", key="ec2c")
                with col2: v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, format="%.3f", key="ev2c")
                hasil = (c2*v2)/v1
                st.markdown(res("C₁ — Konsentrasi awal", f"{hasil:.6g}", satuan, "rc-green"), unsafe_allow_html=True)
            else:
                with col1:
                    c1 = st.number_input("C₁ — Konsentrasi awal", 1e-9, value=1.0, format="%.5f", key="ec1d")
                    c2 = st.number_input("C₂ — Konsentrasi akhir", 0.0, value=0.1, format="%.5f", key="ec2d")
                with col2: v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, format="%.3f", key="ev2d")
                hasil = (c2*v2)/c1
                st.markdown(res("V₁ — Volume awal", f"{hasil:.5g}", "mL", "rc-green"), unsafe_allow_html=True)
        with t1b:
            st.markdown("""<div class="formula-box">C₢ = C₀ × (V_aliquot / V_total)ⁿ</div>""", unsafe_allow_html=True)
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
                rows = "".join(f"<tr><td style='padding:6px 10px'>{'Stok' if i==0 else f'Langkah {i}'}</td><td style='padding:6px 10px;font-family:DM Mono,monospace;color:#085041'>{c0*(f**i):.4e}</td><td style='padding:6px 10px;color:#888'>{sat_s}</td></tr>" for i in range(int(nstep)+1))
                st.markdown(f"""<table style="width:100%;border-collapse:collapse;border:1px solid #e0e0e0;font-size:13px;margin-top:.5rem;border-radius:10px;overflow:hidden"><thead><tr style="background:#E1F5EE"><th style="padding:8px 10px;text-align:left;color:#085041">Tabung</th><th style="padding:8px 10px;text-align:left;color:#085041">Konsentrasi</th><th style="padding:8px 10px;text-align:left;color:#085041">Satuan</th></tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)
        with t1c:
            col1, col2 = st.columns(2)
            with col1:
                va_fp = st.number_input("Volume awal (mL)",  0.001, value=1.0, format="%.3f", key="fp_va")
                vb_fp = st.number_input("Volume akhir (mL)", 0.001, value=100.0, format="%.3f", key="fp_vb")
            with col2: ca_fp = st.number_input("Konsentrasi awal (opsional)", 0.0, value=1.0, format="%.5f", key="fp_ca")
            fp = vb_fp / va_fp
            st.markdown(res("Faktor Pengenceran", f"1 : {fp:.4f}", "", "rc-green"), unsafe_allow_html=True)
            st.markdown(res("Konsentrasi Akhir", f"{ca_fp/fp:.5g}", "", "rc-green"), unsafe_allow_html=True)

    # MODUL 2 — STOIKIOMETRI
    elif st.session_state.menu_aktif == "Stoikiometri":
        st.markdown("### ⇌ Satuan Konsentrasi & Stoikiometri")
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
                st.markdown(res("Hasil Konversi", f"{hasil:.6g}", ke, "rc-blue"), unsafe_allow_html=True)
        with t2b:
            cari_m = st.selectbox("Cari:", ["Mol (n) dari massa & Mr","Mol (n) dari M & V","Massa (g) dari n & Mr","Molaritas (M) dari n & V","Volume (mL) dari n & M"], key="mol_cari")
            col1, col2 = st.columns(2)
            if "massa" in cari_m:
                with col1: massa = st.number_input("Massa (gram)", 0.0, value=5.85, format="%.4f", key="mol_ma")
                with col2: mr2 = st.number_input("Mr (g/mol)", 0.001, value=58.44, key="mol_mr")
                st.markdown(res("Mol (n)", f"{massa/mr2:.5g}", "mol", "rc-blue"), unsafe_allow_html=True)
            elif "M & V" in cari_m:
                with col1: Mm = st.number_input("Molaritas (M)", 0.0, value=1.0, key="mol_Mm")
                with col2: Vm = st.number_input("Volume (mL)", 0.0, value=100.0, key="mol_Vm")
                st.markdown(res("Mol (n)", f"{Mm*(Vm/1000):.5g}", "mol", "rc-blue"), unsafe_allow_html=True)
            elif "Massa" in cari_m:
                with col1: nm = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_nm")
                with col2: mr3 = st.number_input("Mr (g/mol)", 0.001, value=58.44, key="mol_mr3")
                st.markdown(res("Massa (m)", f"{nm*mr3:.5g}", "gram", "rc-blue"), unsafe_allow_html=True)
            elif "Molaritas" in cari_m:
                with col1: nm = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_nm2")
                with col2: Vm = st.number_input("Volume (mL)", 0.001, value=100.0, key="mol_Vm2")
                st.markdown(res("Molaritas (M)", f"{nm/(Vm/1000):.5g}", "mol/L", "rc-blue"), unsafe_allow_html=True)
            else:
                with col1: nm = st.number_input("Mol (n)", 0.0, value=0.1, key="mol_nm3")
                with col2: Mm = st.number_input("Molaritas (M)", 0.001, value=1.0, key="mol_Mm3")
                st.markdown(res("Volume (V)", f"{(nm/Mm)*1000:.5g}", "mL", "rc-blue"), unsafe_allow_html=True)
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
            st.markdown(res(f"Hasil {nC}", f"{nC_mol:.5g} mol ({nC_mol*mC:.5g} g)", "", "rc-blue"), unsafe_allow_html=True)

    # MODUL 3 — pH KESETIMBANGAN
    elif st.session_state.menu_aktif == "pH":
        st.markdown("### 📈 Kesetimbangan & Perubahan pH")
        t3a, t3b, t3c, t3d = st.tabs(["🔴 pH Asam", "🔵 pH Basa", "🔬 Hitung Ka/Kb", "📉 ΔpH Pengenceran"])
        with t3a:
            jenis_a = st.radio("Jenis asam:", ["Asam Kuat","Asam Lemah"], horizontal=True)
            Ca = st.number_input("Konsentrasi C (M)", 1e-14, value=0.1, key="as_C")
            if jenis_a == "Asam Kuat": pH = -math.log10(max(Ca, 1e-14))
            else:
                Ka_a = st.number_input("Ka", 1e-20, value=1.8e-5, key="as_Ka")
                pH = -math.log10(math.sqrt(Ka_a * Ca))
            st.markdown(res("pH Larutan", f"{pH:.4f}", "", "rc-amber"), unsafe_allow_html=True)
            st.markdown(ph_bar(pH), unsafe_allow_html=True)
        with t3b:
            jenis_b = st.radio("Jenis basa:", ["Basa Kuat","Basa Lemah"], horizontal=True)
            Cb = st.number_input("Konsentrasi C (M)", 1e-14, value=0.1, key="bs_C")
            if jenis_b == "Basa Kuat": pH = 14 + math.log10(Cb)
            else:
                Kb_b = st.number_input("Kb", 1e-20, value=1.8e-5, key="bs_Kb")
                pH = 14 + math.log10(math.sqrt(Kb_b * Cb))
            st.markdown(res("pH Larutan", f"{pH:.4f}", "", "rc-amber"), unsafe_allow_html=True)
            st.markdown(ph_bar(pH), unsafe_allow_html=True)
        with t3c:
            Ck = st.number_input("Konsentrasi C (M)", 1e-10, value=0.1, key="kk_C")
            pHk = st.number_input("pH terukur", 0.0, 14.0, value=2.87, key="kk_pH")
            H = 10**(-pHk)
            if Ck > H: st.markdown(res("Ka Prediksi", f"{H**2 / (Ck - H):.4e}", "", "rc-amber"), unsafe_allow_html=True)
        with t3d:
            jenis_d = st.radio("Jenis larutan:", ["Asam Kuat","Asam Lemah","Basa Kuat","Basa Lemah"], horizontal=True, key="dp_j")
            kode_d  = {"Asam Kuat":"ak","Asam Lemah":"al","Basa Kuat":"bk","Basa Lemah":"bl"}[jenis_d]
            C1d = st.number_input("C₁ (M)", 1e-14, value=0.1, key="dp_C1")
            V1d = st.number_input("V₁ (mL)", 0.001, value=10.0, key="dp_V1")
            V2d = st.number_input("V₂ (mL)", 0.001, value=100.0, key="dp_V2")
            Kd = st.number_input("Ka / Kb", 1e-20, value=1.8e-5, key="dp_K") if "Lemah" in jenis_d else None
            pH1 = calc_ph(kode_d, C1d, Kd)
            pH2 = calc_ph(kode_d, (C1d*V1d/V2d), Kd)
            st.markdown(res("pH Akhir", f"{pH2:.4f} (Awal: {pH1:.4f})", "", "rc-amber"), unsafe_allow_html=True)

    # MODUL 4 — LARUTAN BUFFER
    elif st.session_state.menu_aktif == "Buffer":
        st.markdown("### 🧪 Pembuatan Larutan Buffer")
        t4a, t4b, t4c = st.tabs(["🧮 Hitung pH Buffer", "⚖️ Hitung Rasio [A⁻]/[HA]", "📊 Kapasitas Buffer (β)"])
        with t4a:
            pKa_b = st.number_input("pKa asam", 0.0, 14.0, value=4.74)
            ab = st.number_input("[A⁻] Basa Konjugat (M)", 0.0001, value=0.1)
            ha = st.number_input("[HA] Asam (M)", 0.0001, value=0.1)
            st.markdown(res("pH Buffer", f"{pKa_b + math.log10(ab / ha):.4f}", "", "rc-purple"), unsafe_allow_html=True)
        with t4b:
            pHt = st.number_input("pH target", 0.0, 14.0, value=5.0)
            pKa_r = st.number_input("pKa asam", 0.0, 14.0, value=4.74, key="br_pka")
            Ctot = st.number_input("Konsentrasi total (M)", 0.001, value=0.2)
            ratio = 10**(pHt - pKa_r)
            st.markdown(res("Rasio [A⁻]/[HA]", f"{ratio:.5f}", f"([A⁻]={Ctot*ratio/(1+ratio):.4f}M)", "rc-purple"), unsafe_allow_html=True)
        with t4c:
            Cbc = st.number_input("Konsentrasi total (M)", 0.0001, value=0.1, key="bc_C")
            Ka_bc = st.number_input("Ka", 1e-20, value=1.8e-5, key="bc_Ka")
            pH_bc = st.number_input("pH larutan", 0.0, 14.0, value=4.74, key="bc_pH")
            H_bc = 10**(-pH_bc)
            beta = 2.303 * Cbc * (Ka_bc * H_bc) / (Ka_bc + H_bc)**2
            st.markdown(res("Kapasitas Buffer (β)", f"{beta:.4e}", "", "rc-purple"), unsafe_allow_html=True)

    # MODUL 5 — ANALISIS GALAT
    elif st.session_state.menu_aktif == "Galat":
        st.markdown("### ± Galat & Propagasi Error")
        t5a, t5b, t5c = st.tabs(["📏 Galat Absolut & Relatif", "⚡ Propagasi Error", "📊 Statistik (SD & RSD)"])
        with t5a:
            xu = st.number_input("Nilai terukur", value=9.87)
            xb = st.number_input("Nilai benar", value=10.00)
            st.markdown(res("Galat Absolut", f"{abs(xu-xb):.5g}", "", "rc-coral"), unsafe_allow_html=True)
        with t5b:
            op = st.selectbox("Operasi:", ["Penjumlahan / Pengurangan (x ± y)", "Perkalian / Pembagian (x × y atau x/y)"])
            x_val = st.number_input("Nilai x", value=10.0)
            dx_val = st.number_input("δx", value=0.05)
            y_val = st.number_input("Nilai y", value=5.0)
            dy_val = st.number_input("δy", value=0.03)
            if "Penjumlahan" in op: st.markdown(res("Ketidakpastian Akhir", f"± {math.sqrt(dx_val**2 + dy_val**2):.5g}", "", "rc-coral"), unsafe_allow_html=True)
            else: st.markdown(res("Ketidakpastian Akhir", f"± {(x_val*y_val)*math.sqrt((dx_val/x_val)**2 + (dy_val/y_val)**2):.5g}", "", "rc-coral"), unsafe_allow_html=True)
        with t5c:
            raw = st.text_area("Data pengukuran (pisahkan dengan koma):", value="9.87, 9.92, 9.85, 9.90, 9.88")
            arr = [float(t.strip()) for t in raw.split(',') if t.strip()]
            if len(arr) >= 2:
                mean_s = sum(arr)/len(arr)
                sd_s = math.sqrt(sum((xi-mean_s)**2 for xi in arr)/(len(arr)-1))
                st.markdown(res("Rata-rata ± SD", f"{mean_s:.4g} ± {sd_s:.4g}", f"(RSD: {sd_s/mean_s*100:.3f}%)", "rc-coral"), unsafe_allow_html=True)


# ==========================================
# FOOTER HALAMAN
# ==========================================
st.divider()
st.markdown('<p style="text-align:center;font-size:12px;color:#b0b0b0">⚗️ Kalkulator Analisis Kuantitatif · Kimia Analitik</p>', unsafe_allow_html=True)

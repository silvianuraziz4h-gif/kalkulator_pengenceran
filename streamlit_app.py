import streamlit as st
import math

# 1. PENGENTURAN HALAMAN (Cukup dipanggil 1 kali di paling atas)
st.set_page_config(
    page_title="Kalkulator Analisis Kuantitatif",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. GAYA CSS CUSTOM (Disederhanakan dan dirapikan)
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

/* Identitas warna per modul kalkulator */
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

div.stTabs [data-baseweb="tab-list"] { gap:6px; }
div.stTabs [data-baseweb="tab"] { border-radius:8px 8px 0 0; padding: 10px 16px; }
</style>
""", unsafe_allow_html=True)

# 3. FUNGSI LOGIKA / HELPERS
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


# 4. ELEMEN HEADER ATAS
st.markdown('<div class="badge">⚗ Kimia Analitik</div>', unsafe_allow_html=True)
st.markdown("""
<h1 class="main-title">Kalkulator <em>Analisis</em> Kuantitatif</h1>
<p class="subtitle">Alat perhitungan terintegrasi untuk kimia analitik. Klik pada tab topik di bawah ini untuk langsung membuka kalkulator spesifik.</p>
""", unsafe_allow_html=True)
st.divider()


# 5. PEMBUATAN TABS UTAMA (Menyatukan Topik & Kalkulator secara Horizontal)
M1, M2, M3, M4, M5 = st.tabs([
    "💧 01. Pengenceran Larutan",
    "⇌ 02. Konsentrasi & Stoikiometri",
    "📈 03. Kesetimbangan & pH",
    "🧪 04. Larutan Buffer",
    "± 05. Galat & Propagasi"
])

# ==========================================
# MODUL 1 — PENGENCERAN
# ==========================================
with M1:
    st.markdown("### 💧 Pengenceran Larutan")
    st.caption("Hitung volume atau konsentrasi pada proses pengenceran tunggal maupun bertingkat menggunakan hukum $C_1V_1 = C_2V_2$.")
    
    t1a, t1b, t1c = st.tabs(["C₁V₁ = C₂V₂", "Serial / Bertingkat", "Faktor Pengenceran"])

    with t1a:
        st.markdown('<div class="formula-box">C₁ × V₁ = C₂ × V₂</div>', unsafe_allow_html=True)
        cari   = st.selectbox("Variabel yang dicari:", ["C₂ — Konsentrasi akhir","V₂ — Volume akhir","C₁ — Konsentrasi awal","V₁ — Volume awal"], key="e_cari")
        satuan = st.selectbox("Satuan konsentrasi:", ["M","mM","µM","mg/mL","ppm","ppb"], key="e_sat")
        c1 = c2 = v1 = v2 = None
        col1, col2 = st.columns(2)
        if cari == "C₂ — Konsentrasi akhir":
            with col1:
                c1 = st.number_input("C₁ — Konsentrasi awal", 0.0, value=1.0, step=0.001, format="%.5f", key="ec1a")
                v1 = st.number_input("V₁ — Volume awal (mL)",  0.0, value=10.0, step=0.1,  format="%.3f",  key="ev1a")
            with col2:
                v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, step=1.0, format="%.3f", key="ev2a")
            hasil = (c1*v1)/v2
            st.markdown(res("C₂ — Konsentrasi akhir", f"{hasil:.6g}", satuan, "rc-green"), unsafe_allow_html=True)
            st.markdown(step(f"C₂ = (C₁×V₁)/V₂ = ({c1}×{v1})/{v2} = <b>{hasil:.6g} {satuan}</b>"), unsafe_allow_html=True)

        elif cari == "V₂ — Volume akhir":
            with col1:
                c1 = st.number_input("C₁ — Konsentrasi awal", 0.0, value=1.0,  step=0.001, format="%.5f", key="ec1b")
                v1 = st.number_input("V₁ — Volume awal (mL)",  0.0, value=10.0, step=0.1,   format="%.3f", key="ev1b")
            with col2:
                c2 = st.number_input("C₂ — Konsentrasi akhir", 1e-9, value=0.1, step=0.001, format="%.5f", key="ec2b")
            hasil = (c1*v1)/c2
            st.markdown(res("V₂ — Volume akhir", f"{hasil:.5g}", "mL", "rc-green"), unsafe_allow_html=True)
            st.markdown(step(f"V₂ = (C₁×V₁)/C₂ = ({c1}×{v1})/{c2} = <b>{hasil:.5g} mL</b>"), unsafe_allow_html=True)

        elif cari == "C₁ — Konsentrasi awal":
            with col1:
                v1 = st.number_input("V₁ — Volume awal (mL)",  1e-9, value=10.0,  step=0.1,  format="%.3f", key="ev1c")
                c2 = st.number_input("C₂ — Konsentrasi akhir", 0.0,  value=0.1,   step=0.001,format="%.5f", key="ec2c")
            with col2:
                v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, step=1.0,  format="%.3f", key="ev2c")
            hasil = (c2*v2)/v1
            st.markdown(res("C₁ — Konsentrasi awal", f"{hasil:.6g}", satuan, "rc-green"), unsafe_allow_html=True)
            st.markdown(step(f"C₁ = (C₂×V₂)/V₁ = ({c2}×{v2})/{v1} = <b>{hasil:.6g} {satuan}</b>"), unsafe_allow_html=True)

        else:
            with col1:
                c1 = st.number_input("C₁ — Konsentrasi awal", 1e-9, value=1.0,   step=0.001, format="%.5f", key="ec1d")
                c2 = st.number_input("C₂ — Konsentrasi akhir", 0.0, value=0.1,   step=0.001, format="%.5f", key="ec2d")
            with col2:
                v2 = st.number_input("V₂ — Volume akhir (mL)", 1e-9, value=100.0, step=1.0,  format="%.3f", key="ev2d")
            hasil = (c2*v2)/c1
            st.markdown(res("V₁ — Volume awal", f"{hasil:.5g}", "mL", "rc-green"), unsafe_allow_html=True)
            st.markdown(step(f"V₁ = (C₂×V₂)/C₁ = ({c2}×{v2})/{c1} = <b>{hasil:.5g} mL</b>"), unsafe_allow_html=True)

    with t1b:
        st.markdown('<div class="formula-box">C₢ = C₀ × (V_aliquot / V_total)ⁿ</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            c0    = st.number_input("C₀ — Konsentrasi stok", 0.0, value=1.0, step=0.01, format="%.5f", key="s_c0")
            nstep = st.number_input("Jumlah langkah", 1, 15, value=5, step=1, key="s_n")
        with col2:
            va_s  = st.number_input("Volume aliquot (mL)",          0.001, value=1.0,  step=0.1, format="%.3f", key="s_va")
            vt_s  = st.number_input("Volume total tiap tabung (mL)", 0.001, value=10.0, step=0.1, format="%.3f", key="s_vt")
            sat_s = st.selectbox("Satuan", ["M","mM","µM","mg/mL","ppm"], key="s_sat")
        if va_s >= vt_s:
            st.warning("Volume aliquot harus lebih kecil dari volume total.")
        else:
            f = va_s / vt_s
            st.info(f"Faktor tiap langkah: **1 : {vt_s/va_s:.1f}** | f = {f:.4f}")
            rows = "".join(
                f"<tr><td style='padding:6px 10px'>{'Stok' if i==0 else f'Langkah {i}'}</td>"
                f"<td style='padding:6px 10px;font-family:DM Mono,monospace;color:#085041'>{c0*(f**i):.4e}</td>"
                f"<td style='padding:6px 10px;color:#888'>{sat_s}</td>"
                f"<td style='padding:6px 10px;font-family:DM Mono,monospace;color:#aaa'>{f**i:.3e}</td></tr>"
                for i in range(int(nstep)+1)
            )
            st.markdown(f"""<table style="width:100%;border-collapse:collapse;border:1px solid #e0e0e0;font-size:13px;margin-top:.5rem;border-radius:10px;overflow:hidden">
              <thead><tr style="background:#E1F5EE"><th style="padding:8px 10px;text-align:left;color:#085041">Tabung</th>
              <th style="padding:8px 10px;text-align:left;color:#085041">Konsentrasi</th>
              <th style="padding:8px 10px;text-align:left;color:#085041">Satuan</th>
              <th style="padding:8px 10px;text-align:left;color:#085041">Faktor</th></tr></thead>
              <tbody>{rows}</tbody></table>""", unsafe_allow_html=True)

    with t1c:
        st.markdown('<div class="formula-box">FP = V_akhir / V_awal &nbsp;|&nbsp; C_akhir = C_awal / FP</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            va_fp = st.number_input("Volume awal (mL)",  0.001, value=1.0,   step=0.1,  format="%.3f", key="fp_va")
            vb_fp = st.number_input("Volume akhir (mL)", 0.001, value=100.0, step=1.0,  format="%.3f", key="fp_vb")
        with col2:
            ca_fp = st.number_input("Konsentrasi awal (opsional)", 0.0, value=1.0, step=0.001, format="%.5f", key="fp_ca")
        fp  = vb_fp / va_fp
        ca2 = ca_fp / fp
        st.markdown(res("Faktor Pengenceran", f"1 : {fp:.4f}", "", "rc-green"), unsafe_allow_html=True)
        st.markdown(res("Konsentrasi Akhir", f"{ca2:.5g}", "", "rc-green"), unsafe_allow_html=True)
        st.markdown(step(f"FP = {vb_fp}/{va_fp} = <b>{fp:.4f}</b><br>C_akhir = {ca_fp}/{fp:.4f} = <b>{ca2:.5g}</b>"), unsafe_allow_html=True)

# ==========================================
# MODUL 2 — KONSENTRASI & STOIKIOMETRI
# ==========================================
with M2:
    st.markdown("### ⇌ Satuan Konsentrasi & Stoikiometri")
    st.caption("Konversi antar satuan konsentrasi (M, m, %, ppm, ppb) dan hitung hubungan hubungan mol ratio dalam stoikiometri.")
    
    t2a, t2b, t2c = st.tabs(["🔄 Konversi Satuan", "⚖️ Mol & Massa", "🧮 Stoikiometri Reaksi"])

    with t2a:
        st.markdown('<div class="formula-box">M = n/V &nbsp;|&nbsp; ppm = mg/L &nbsp;|&nbsp; % m/v = g/100mL &nbsp;|&nbsp; ppb = µg/L</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            dari  = st.selectbox("Dari satuan:", SATUAN_KONSENTRASI, index=0, key="k_dari")
            nilai = st.number_input("Nilai", 0.0, value=1.0, step=0.0001, format="%.6f", key="k_val")
            mr_k  = st.number_input("Mr zat (g/mol)", 0.001, value=58.44, step=0.01, format="%.3f", key="k_mr")
        with col2:
            ke   = st.selectbox("Ke satuan:", SATUAN_KONSENTRASI, index=2, key="k_ke")
            rho  = st.number_input("Densitas ρ (g/mL)", 0.001, value=1.0, step=0.001, format="%.4f", key="k_rho")
        if dari == ke:
            st.warning("Pilih satuan yang berbeda.")
        else:
            mgL   = to_mgL(nilai, dari, mr_k, rho)
            hasil = from_mgL(mgL, ke, mr_k, rho)
            st.markdown(res("Hasil Konversi", f"{hasil:.6g}", ke, "rc-blue"), unsafe_allow_html=True)
            st.markdown(step(f"{nilai} {dari}<br>→ {mgL:.4g} mg/L (basis)<br>→ <b>{hasil:.6g} {ke}</b><br>Mr={mr_k} g/mol | ρ={rho} g/mL"), unsafe_allow_html=True)

    with t2b:
        st.markdown('<div class="formula-box">n = m/Mr &nbsp;|&nbsp; n = M×V &nbsp;|&nbsp; m = n×Mr &nbsp;|&nbsp; M = n/V</div>', unsafe_allow_html=True)
        cari_m = st.selectbox("Cari:", ["Mol (n) dari massa & Mr","Mol (n) dari M & V","Massa (g) dari n & Mr","Molaritas (M) dari n & V","Volume (mL) dari n & M"], key="mol_cari")
        col1, col2 = st.columns(2)
        if cari_m == "Mol (n) dari massa & Mr":
            with col1: massa = st.number_input("Massa (gram)", 0.0, value=5.85, step=0.01, format="%.4f", key="mol_ma")
            with col2: mr2   = st.number_input("Mr (g/mol)",   0.001, value=58.44, step=0.01, format="%.3f", key="mol_mr")
            n = massa / mr2
            st.markdown(res("Mol (n)", f"{n:.5g}", "mol", "rc-blue"), unsafe_allow_html=True)
            st.markdown(step(f"n = m/Mr = {massa}/{mr2} = <b>{n:.5g} mol</b>"), unsafe_allow_html=True)
        elif cari_m == "Mol (n) dari M & V":
            with col1: Mm = st.number_input("Molaritas (M)", 0.0, value=1.0, step=0.001, format="%.4f", key="mol_Mm")
            with col2: Vm = st.number_input("Volume (mL)",   0.0, value=100.0, step=1.0, format="%.2f", key="mol_Vm")
            n = Mm * (Vm/1000)
            st.markdown(res("Mol (n)", f"{n:.5g}", "mol", "rc-blue"), unsafe_allow_html=True)
            st.markdown(step(f"n = M×V(L) = {Mm}×{Vm/1000} = <b>{n:.5g} mol</b>"), unsafe_allow_html=True)
        elif cari_m == "Massa (g) dari n & Mr":
            with col1: nm = st.number_input("Mol (n)",    0.0, value=0.1, step=0.001, format="%.5f", key="mol_nm")
            with col2: mr3= st.number_input("Mr (g/mol)", 0.001, value=58.44, step=0.01, format="%.3f", key="mol_mr3")
            m = nm * mr3
            st.markdown(res("Massa (m)", f"{m:.5g}", "gram", "rc-blue"), unsafe_allow_html=True)
            st.markdown(step(f"m = n×Mr = {nm}×{mr3} = <b>{m:.5g} g</b>"), unsafe_allow_html=True)
        elif cari_m == "Molaritas (M) dari n & V":
            with col1: nm = st.number_input("Mol (n)",    0.0, value=0.1, step=0.001, format="%.5f", key="mol_nm2")
            with col2: Vm = st.number_input("Volume (mL)",0.001, value=100.0, step=1.0, format="%.2f", key="mol_Vm2")
            M2 = nm / (Vm/1000)
            st.markdown(res("Molaritas (M)", f"{M2:.5g}", "mol/L", "rc-blue"), unsafe_allow_html=True)
            st.markdown(step(f"M = n/V(L) = {nm}/{Vm/1000} = <b>{M2:.5g} mol/L</b>"), unsafe_allow_html=True)
        else:
            with col1: nm = st.number_input("Mol (n)",        0.0,  value=0.1, step=0.001, format="%.5f", key="mol_nm3")
            with col2: Mm = st.number_input("Molaritas (M)",  0.001, value=1.0, step=0.001, format="%.4f", key="mol_Mm3")
            V2 = (nm/Mm)*1000
            st.markdown(res("Volume (V)", f"{V2:.5g}", "mL", "rc-blue"), unsafe_allow_html=True)
            st.markdown(step(f"V = (n/M)×1000 = ({nm}/{Mm})×1000 = <b>{V2:.5g} mL</b>"), unsafe_allow_html=True)

    with t2c:
        st.markdown('<div class="formula-box">aA + bB → cC + dD &nbsp;|&nbsp; n_hasil = n_reaktan × (koef_hasil / koef_reaktan)</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kA = st.number_input("Koef A", 1, value=1, step=1, key="stA_k")
            nA = st.text_input("Nama A", "HCl",  key="stA_n")
            mA = st.number_input("Mr A",  0.001, value=36.46, step=0.01, format="%.3f", key="stA_m")
        with col2:
            kB = st.number_input("Koef B", 1, value=1, step=1, key="stB_k")
            nB = st.text_input("Nama B", "NaOH", key="stB_n")
            mB = st.number_input("Mr B",  0.001, value=40.00, step=0.01, format="%.3f", key="stB_m")
        with col3:
            kC = st.number_input("Koef C", 1, value=1, step=1, key="stC_k")
            nC = st.text_input("Nama C", "NaCl", key="stC_n")
            mC = st.number_input("Mr C",  0.001, value=58.44, step=0.01, format="%.3f", key="stC_m")
        with col4:
            kD = st.number_input("Koef D", 1, value=1, step=1, key="stD_k")
            nD = st.text_input("Nama D", "H₂O", key="stD_n")
            mD = st.number_input("Mr D",  0.001, value=18.02, step=0.01, format="%.3f", key="stD_m")
        st.info(f"**Reaksi:** {kA} {nA} + {kB} {nB} → {kC} {nC} + {kD} {nD}")
        col1, col2 = st.columns(2)
        with col1:
            zat_r  = st.selectbox("Reaktan pembatas:", [nA, nB], key="st_zat")
            mode_r = st.radio("Diketahui dalam:", ["Massa (g)","Mol","M + V"], horizontal=True, key="st_mode")
        with col2:
            if mode_r == "Massa (g)":
                massa_r = st.number_input("Massa (g)", 0.0, value=3.65, step=0.01, format="%.4f", key="st_mg")
                mr_ref  = mA if zat_r == nA else mB
                n_ref   = massa_r / mr_ref
            elif mode_r == "Mol":
                n_ref = st.number_input("Mol", 0.0, value=0.1, step=0.001, format="%.5f", key="st_mol")
            else:
                Ms_ = st.number_input("M (mol/L)", 0.0, value=1.0, step=0.001, format="%.4f", key="st_Ms")
                Vs_ = st.number_input("V (mL)",    0.0, value=100.0, step=1.0, format="%.2f", key="st_Vs")
                n_ref = Ms_ * (Vs_/1000)
        k_ref = kA if zat_r == nA else kB
        nC_mol = n_ref*(kC/k_ref);  mC_g = nC_mol*mC
        nD_mol = n_ref*(kD/k_ref);  mD_g = nD_mol*mD
        n_pas  = n_ref*(kB/kA) if zat_r == nA else n_ref*(kA/kB)
        nm_pas = nB if zat_r == nA else nA;  mr_pas = mB if zat_r == nA else mA
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(res(f"Mol {nC}", f"{nC_mol:.5g} mol → {mC_g:.5g} g", "", "rc-blue"), unsafe_allow_html=True)
        with col2:
            st.markdown(res(f"Mol {nD}", f"{nD_mol:.5g} mol → {mD_g:.5g} g", "", "rc-blue"), unsafe_allow_html=True)
        st.markdown(step(f"n({zat_r}) = {n_ref:.5g} mol<br>n({nC}) = {n_ref:.4g}×({kC}/{k_ref}) = <b>{nC_mol:.5g} mol</b> → <b>{mC_g:.5g} g</b><br>n({nD}) = {n_ref:.4g}×({kD}/{k_ref}) = <b>{nD_mol:.5g} mol</b> → <b>{mD_g:.5g} g</b><br>Kebutuhan {nm_pas} = {n_pas:.5g} mol = <b>{n_pas*mr_pas:.5g} g</b>"), unsafe_allow_html=True)

# ==========================================
# MODUL 3 — KESETIMBANGAN & pH
# ==========================================
with M3:
    st.markdown("### 📈 Kesetimbangan & Perubahan pH")
    st.caption("Prediksi kesetimbangan asam-basa, konstanta $K_a/K_b$, serta simulasi perubahan delta pH setelah proses pengenceran larutan.")
    
    t3a, t3b, t3c, t3d = st.tabs(["🔴 pH Asam", "🔵 pH Basa", "🔬 Hitung Ka/Kb", "📉 ΔpH Pengenceran"])

    with t3a:
        jenis_a = st.radio("Jenis asam:", ["Asam Kuat","Asam Lemah"], horizontal=True, key="as_j")
        col1, col2 = st.columns(2)
        with col1:
            Ca = st.number_input("Konsentrasi C (M)", 1e-14, value=0.1, step=0.001, format="%.6f", key="as_C")
        if jenis_a == "Asam Kuat":
            st.markdown('<div class="formula-box">pH = −log[H⁺] = −log C</div>', unsafe_allow_html=True)
            pH = -math.log10(max(Ca, 1e-14))
            st.markdown(res("pH larutan", f'<span style="color:{ph_color(pH)}">{pH:.4f}</span>', "", "rc-amber"), unsafe_allow_html=True)
            st.markdown(ph_bar(pH), unsafe_allow_html=True)
            st.markdown(step(f"[H⁺] = {Ca} M<br>pH = −log({Ca}) = <b>{pH:.4f}</b>"), unsafe_allow_html=True)
        else:
            st.markdown('<div class="formula-box">HA ⇌ H⁺ + A⁻ &nbsp;|&nbsp; [H⁺] = √(Ka × C)</div>', unsafe_allow_html=True)
            with col2:
                Ka_a = st.number_input("Ka", 1e-20, value=1.8e-5, step=1e-7, format="%.2e", key="as_Ka")
            H   = math.sqrt(Ka_a * Ca)
            pH  = -math.log10(max(H, 1e-14))
            pKa = -math.log10(Ka_a)
            st.markdown(res("pH larutan", f'<span style="color:{ph_color(pH)}">{pH:.4f}</span>', "", "rc-amber"), unsafe_allow_html=True)
            st.markdown(ph_bar(pH), unsafe_allow_html=True)
            st.markdown(step(f"Ka={Ka_a:.3e} | pKa={pKa:.4f}<br>[H⁺]=√({Ka_a:.3e}×{Ca})={H:.4e} M<br>α={H/Ca*100:.3f}%<br>pH=−log({H:.4e})=<b>{pH:.4f}</b>"), unsafe_allow_html=True)

    with t3b:
        jenis_b = st.radio("Jenis basa:", ["Basa Kuat","Basa Lemah"], horizontal=True, key="bs_j")
        col1, col2 = st.columns(2)
        with col1:
            Cb = st.number_input("Konsentrasi C (M)", 1e-14, value=0.1, step=0.001, format="%.6f", key="bs_C")
        if jenis_b == "Basa Kuat":
            st.markdown('<div class="formula-

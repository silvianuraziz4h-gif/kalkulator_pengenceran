import streamlit as st

# Pengaturan halaman utama
st.set_page_config(
    page_title="Kalkulator Pengenceran Larutan",
    page_icon="🧪",
    layout="centered"
)

# Judul dan Deskripsi Aplikasi
st.title("🧪 Kalkulator Pengenceran Larutan")
st.write(
    "Gunakan kalkulator ini untuk menghitung volume larutan stok pekat "
    "yang Anda butuhkan untuk membuat larutan dengan konsentrasi dan volume tertentu."
)
st.write("Formula dasar: **M₁ × V₁ = M₂ × V₂**")

st.divider()

# Membuat Grid Layout untuk Input (2 kolom)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Larutan Stok (Awal)")
    m1 = st.number_input("Konsentrasi Awal (M₁)", min_value=0.0, step=0.1, format="%.4f", value=1.0, help="Konsentrasi larutan pekat Anda")
    u_m1 = st.selectbox("Satuan M₁", ["M", "mM", "µM", "%", "mg/mL"], key="u_m1")

with col2:
    st.subheader("Larutan Target (Akhir)")
    m2 = st.number_input("Konsentrasi Target (M₂)", min_value=0.0, step=0.1, format="%.4f", value=0.1, help="Konsentrasi akhir yang Anda inginkan")
    u_m2 = st.selectbox("Satuan M₂", ["M", "mM", "µM", "%", "mg/mL"], key="u_m2")
    
    st.write("---")
    
    v2 = st.number_input("Volume Target (V₂)", min_value=0.0, step=1.0, format="%.2f", value=100.0, help="Volume total larutan akhir yang ingin dibuat")
    u_v2 = st.selectbox("Satuan V₂", ["mL", "L", "µL"], key="u_v2")

st.divider()

# Bagian Kalkulasi
st.subheader("Hasil Perhitungan (V₁)")

# Logika validasi input dasar
if m1 <= 0 or m2 <= 0 or v2 <= 0:
    st.warning("Silakan masukkan nilai yang lebih besar dari 0 pada semua kolom input.")
elif u_m1 != u_m2:
    st.error("⚠️ Perhatian: Pastikan satuan konsentrasi M₁ dan M₂ sama (misal: sama-sama M atau sama-sama %). Aplikasi ini menggunakan basis rasio langsung.")
elif m1 < m2:
    st.error("❌ Error: Konsentrasi awal (M₁) tidak boleh lebih kecil dari konsentrasi target (M₂).")
else:
    # Menghitung V1 menggunakan rumus M1.V1 = M2.V2 -> V1 = (M2 * V2) / M1
    v1 = (m2 * v2) / m1
    
    # Menghitung volume pelarut (air/buffer) yang harus ditambahkan
    v_pelarut = v2 - v1
    
    # Menampilkan hasil dengan kartu metrik yang menarik
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.success(f"**Volume Larutan Stok yang Diambil (V₁):**")
        st.code(f"{v1:.4f} {u_v2}", language="text")
        
    with res_col2:
        st.info(f"**Volume Pelarut yang Ditambahkan:**")
        st.code(f"{v_pelarut:.4f} {u_v2}", language="text")
        
    # Petunjuk Pembuatan
    st.write("### 📝 Petunjuk Pembuatan Larutan:")
    st.info(
        f"Ambil sebanyak **{v1:.4f} {u_v2}** larutan stok dengan konsentrasi **{m1} {u_m1}**, "
        f"kemudian masukkan ke dalam wadah/labu takar. Tambahkan pelarut (seperti akuades) "
        f"sebanyak **{v_pelarut:.4f} {u_v2}** hingga volume total mencapai **{v2} {u_v2}**."
    )

# Footer/Credit
st.caption("Dibuat secara kustom menggunakan Python & Streamlit.")

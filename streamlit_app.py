import streamlit as st

# Pengaturan halaman utama
st.set_page_config(
    page_title="Kalkulator Pengenceran Larutan Advance",
    page_icon="🧪",
    layout="centered"
)

# Judul dan Deskripsi Aplikasi
st.title("🧪 Kalkulator Pengenceran Larutan")
st.write(
    "Kalkulator ini dapat menghitung salah satu variabel dari rumus pengenceran "
    "(**M₁ × V₁ = M₂ × V₂**) dengan konversi satuan otomatis beserta petunjuk pembuatannya."
)

st.divider()

# Kamus Faktor Konversi ke Satuan Dasar (Dasar Konsentrasi: M, Dasar Volume: mL)
KONVERSI_M = {"M": 1.0, "mM": 1e-3, "µM": 1e-6}
KONVERSI_V = {"mL": 1.0, "L": 1000.0, "µL": 1e-3}

# Pilihan Variabel yang Dicari
st.subheader("🔍 Pilih Variabel yang Ingin Dicari")
variabel_dicari = st.selectbox(
    "Saya ingin mencari nilai dari:",
    [
        "Volume Awal yang Dibutuhkan (V₁)", 
        "Konsentrasi Awal / Stok (M₁)", 
        "Volume Akhir / Target (V₂)", 
        "Konsentrasi Akhir / Target (M₂)"
    ]
)

st.divider()

# Grid Layout untuk Input
col1, col2 = st.columns(2)

# Mengondisikan input berdasarkan variabel yang dicari
with col1:
    st.markdown("### **Larutan Stok (Awal)**")
    
    if variabel_dicari != "Konsentrasi Awal / Stok (M₁)":
        m1 = st.number_input("Konsentrasi Awal (M₁)", min_value=0.0, step=0.1, format="%.2f", value=1.0)
        u_m1 = st.selectbox("Satuan M₁", list(KONVERSI_M.keys()), key="u_m1")
    else:
        st.info("🔄 *M₁ akan dihitung oleh sistem*")
        u_m1 = st.selectbox("Satuan Output M₁ yang Diinginkan", list(KONVERSI_M.keys()), key="u_m1")

    if variabel_dicari != "Volume Awal yang Dibutuhkan (V₁)":
        v1 = st.number_input("Volume Awal (V₁)", min_value=0.0, step=1.0, format="%.2f", value=10.0)
        u_v1 = st.selectbox("Satuan V₁", list(KONVERSI_V.keys()), key="u_v1")
    else:
        st.info("🔄 *V₁ akan dihitung oleh sistem*")
        u_v1 = st.selectbox("Satuan Output V₁ yang Diinginkan", list(KONVERSI_V.keys()), key="u_v1")

with col2:
    st.markdown("### **Larutan Target (Akhir)**")
    
    if variabel_dicari != "Konsentrasi Akhir / Target (M₂)":
        m2 = st.number_input("Konsentrasi Target (M₂)", min_value=0.0, step=0.1, format="%.2f", value=0.1)
        u_m2 = st.selectbox("Satuan M₂", list(KONVERSI_M.keys()), key="u_m2")
    else:
        st.info("🔄 *M₂ akan dihitung oleh sistem*")
        u_m2 = st.selectbox("Satuan Output M₂ yang Diinginkan", list(KONVERSI_M.keys()), key="u_m2")

    if variabel_dicari != "Volume Akhir / Target (V₂)":
        v2 = st.number_input("Volume Target (V₂)", min_value=0.0, step=1.0, format="%.2f", value=100.0)
        u_v2 = st.selectbox("Satuan V₂", list(KONVERSI_V.keys()), key="u_v2")
    else:
        st.info("🔄 *V₂ akan dihitung oleh sistem*")
        u_v2 = st.selectbox("Satuan Output V₂ yang Diinginkan", list(KONVERSI_V.keys()), key="u_v2")

st.divider()
st.subheader("📊 Hasil Perhitungan & Petunjuk")

# Logika Perhitungan dengan Konversi Satuan Otomatis
try:
    if variabel_dicari == "Volume Awal yang Dibutuhkan (V₁)":
        if m1 <= 0:
            st.error("Konsentrasi Awal (M₁) harus lebih besar dari 0.")
        else:
            m1_dasar = m1 * KONVERSI_M[u_m1]
            m2_dasar = m2 * KONVERSI_M[u_m2]
            v2_dasar = v2 * KONVERSI_V[u_v2]
            
            if m1_dasar < m2_dasar:
                st.warning("⚠️ Konsentrasi awal (M₁) lebih kecil dari konsentrasi target (M₂). Ini adalah proses pemekatan, bukan pengenceran.")
            
            v1_dasar = (m2_dasar * v2_dasar) / m1_dasar
            v1_hasil = v1_dasar / KONVERSI_V[u_v1]
            
            # Hitung pelarut (v2 - v1) disamakan ke satuan V2 agar serasi di petunjuk
            v1_konv_ke_v2_unit = v1_dasar / KONVERSI_V[u_v2]
            v_pelarut = v2 - v1_konv_ke_v2_unit
            
            st.success(f"**Volume Awal (V₁) yang dibutuhkan:**")
            st.code(f"{v1_hasil:.2f} {u_v1}", language="text")
            
            st.write("### 📝 Petunjuk Pembuatan:")
            if v_pelarut >= 0:
                st.info(
                    f"Ambil sebanyak **{v1_hasil:.2f} {u_v1}** dari larutan stok (konsentrasi **{m1:.2f} {u_m1}**). "
                    f"Masukkan ke wadah baru, lalu tambahkan pelarut (akuades/buffer) sebanyak **{v_pelarut:.2f} {u_v2}** "
                    f"hingga volume total akhir menjadi **{v2:.2f} {u_v2}** untuk mendapatkan konsentrasi **{m2:.2f} {u_m2}**."
                )
            else:
                st.error("Volume awal hasil kalkulasi melebihi volume target. Mohon periksa kembali input Anda.")

    elif variabel_dicari == "Konsentrasi Awal / Stok (M₁)":
        if v1 <= 0:
            st.error("Volume Awal (V₁) harus lebih besar dari 0.")
        else:
            v1_dasar = v1 * KONVERSI_V[u_v1]
            m2_dasar = m2 * KONVERSI_M[u_m2]
            v2_dasar = v2 * KONVERSI_V[u_v2]
            
            m1_dasar = (m2_dasar * v2_dasar) / v1_dasar
            m1_hasil = m1_dasar / KONVERSI_M[u_m1]
            
            st.success(f"**Konsentrasi Awal / Stok (M₁):**")
            st.code(f"{m1_hasil:.2f} {u_m1}", language="text")
            
            # Hitung pelarut
            v_pelarut_dasar = v2_dasar - v1_dasar
            v_pelarut_hasil = v_pelarut_dasar / KONVERSI_V[u_v2]
            
            st.write("### 📝 Petunjuk Analisis:")
            st.info(
                f"Jika Anda mengambil **{v1:.2f} {u_v1}** larutan ini dan menambahkan pelarut sebanyak "
                f"**{v_pelarut_hasil:.2f} {u_v2}** (sampai volume **{v2:.2f} {u_v2}**), Anda akan mendapatkan "
                f"larutan dengan konsentrasi target **{m2:.2f} {u_m2}**. "
                f"Ini membuktikan bahwa larutan stok asal Anda berkonsentrasi **{m1_hasil:.2f} {u_m1}**."
            )

    elif variabel_dicari == "Volume Akhir / Target (V₂)":
        if m2 <= 0:
            st.error("Konsentrasi Target (M₂) harus lebih besar dari 0.")
        else:
            m1_dasar = m1 * KONVERSI_M[u_m1]
            v1_dasar = v1 * KONVERSI_V[u_v1]
            m2_dasar = m2 * KONVERSI_M[u_m2]
            
            v2_dasar = (m1_dasar * v1_dasar) / m2_dasar
            v2_hasil = v2_dasar / KONVERSI_V[u_v2]
            
            # Hitung pelarut
            v_pelarut_dasar = v2_dasar - v1_dasar
            v_pelarut_hasil = v_pelarut_dasar / KONVERSI_V[u_v2]
            
            st.success(f"**Volume Akhir / Target (V₂):**")
            st.code(f"{v2_hasil:.2f} {u_v2}", language="text")
            
            st.write("### 📝 Petunjuk Pembuatan:")
            if v_pelarut_hasil >= 0:
                st.info(
                    f"Ambil seluruh **{v1:.2f} {u_v1}** larutan stok berkonsentrasi **{m1:.2f} {u_m1}**. "
                    f"Tambahkan pelarut sebanyak **{v_pelarut_hasil:.2f} {u_v2}** ke dalamnya. "
                    f"Volume total akan menjadi **{v2_hasil:.2f} {u_v2}** dengan konsentrasi akhir tepat **{m2:.2f} {u_m2}**."
                )
            else:
                st.warning("⚠️ Konsentrasi target lebih tinggi dari konsentrasi awal. Tidak bisa diencerkan.")

    elif variabel_dicari == "Konsentrasi Akhir / Target (M₂)":
        if v2 <= 0:
            st.error("Volume Target (V₂) harus lebih besar dari 0.")
        else:
            m1_dasar = m1 * KONVERSI_M[u_m1]
            v1_dasar = v1 * KONVERSI_V[u_v1]
            v2_dasar = v2 * KONVERSI_V[u_v2]
            
            m2_dasar = (m1_dasar * v1_dasar) / v2_dasar
            m2_hasil = m2_dasar / KONVERSI_M[u_m2]
            
            st.success(f"**Konsentrasi Akhir / Target (M₂):**")
            st.code(f"{m2_hasil:.2f} {u_m2}", language="text")
            
            # Hitung pelarut
            v_pelarut_dasar = v2_dasar - v1_dasar
            v_pelarut_hasil = v_pelarut_dasar / KONVERSI_V[u_v2]
            
            st.write("### 📝 Petunjuk Pembuatan:")
            if v_pelarut_hasil >= 0:
                st.info(
                    f"Campurkan **{v1:.2f} {u_v1}** larutan stok (konsentrasi **{m1:.2f} {u_m1}**) dengan pelarut "
                    f"sebanyak **{v_pelarut_hasil:.2f} {u_v2}** hingga wadah terisi tepat pada batas volume **{v2:.2f} {u_v2}**. "
                    f"Larutan baru yang terbentuk akan memiliki konsentrasi **{m2_hasil:.2f} {u_m2}**."
                )
            else:
                st.warning("⚠️ Volume target lebih kecil dari volume awal. Ini bukan proses pengenceran biasa.")

except Exception as e:
    st.error(f"Terjadi kesalahan dalam perhitungan: {e}")

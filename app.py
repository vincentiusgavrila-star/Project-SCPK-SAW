import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="SPK Nasabah Kartu Kredit",
    page_icon="💳",
    layout="wide"
)

# =========================================================
# SIMPLE CSS
# =========================================================
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}

h1, h2, h3 {
    color: #1f2937;
}

[data-testid="stSidebar"] {
    background-color: #54595c;
}

.stButton button {
    border-radius: 8px;
    background-color: #2563eb;
    color: white;
    border: none;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
df = pd.read_csv("BankChurners.csv")

# =========================================================
# KRITERIA SAW
# =========================================================
CRITERIA_COLS = [
    'Credit_Limit',
    'Total_Trans_Amt',
    'Total_Trans_Ct',
    'Months_on_book',
    'Avg_Utilization_Ratio',
    'Total_Relationship_Count',
    'Contacts_Count_12_mon',
    'Months_Inactive_12_mon'
]

CRITERIA_LABELS = [
    'Credit Limit',
    'Total Trans Amt',
    'Total Trans Ct',
    'Months on Book',
    'Avg Util Ratio',
    'Relationship Count',
    'Contacts 12M',
    'Inactive 12M'
]

# 1 = benefit
# 0 = cost
CRITERIA_TYPE = [1,1,1,1,0,1,0,0]

DEFAULT_WEIGHTS = [0.20,0.25,0.15,0.10,0.10,0.10,0.05,0.05]

# =========================================================
# HEADER
# =========================================================
st.title("Sistem Pendukung Keputusan Nasabah Kartu Kredit")
st.write("Metode Simple Additive Weighting (SAW)")

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("Menu Navigasi")

menu = st.sidebar.radio(
    "",
    ["Dataset", "Perhitungan SAW", "Visualisasi", "Profil Kelompok"]
)

# =========================================================
# TAB 1
# =========================================================
if menu == "Dataset":
    st.subheader("Informasi Dataset")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jumlah Data", len(df))
    with col2:
        st.metric("Jumlah Kolom", len(df.columns))
    with col3:
        st.metric("Jumlah Kriteria", len(CRITERIA_COLS))

    st.subheader("Dataset")
    st.dataframe(df.head(100), use_container_width=True)

    st.subheader("Statistik Deskriptif")
    st.dataframe(
        df[CRITERIA_COLS].describe(),
        use_container_width=True
    )

    # =====================================================
    # PIE CHART
    # =====================================================
    st.subheader("Distribusi Status Nasabah")
    fig, ax = plt.subplots()
    vals = df['Attrition_Flag'].value_counts()
    ax.pie(
        vals,
        labels=vals.index,
        autopct='%1.1f%%'
    )
    st.pyplot(fig)

    # =====================================================
    # HISTOGRAM
    # =====================================================
    st.subheader("Distribusi Umur Nasabah")
    fig, ax = plt.subplots(figsize=(10,4))
    ax.hist(df['Customer_Age'], bins=20, edgecolor='white')
    ax.axvline(df['Customer_Age'].mean(), color='red', linestyle='--', linewidth=2, label=f"Rata-rata: {df['Customer_Age'].mean():.0f} tahun")
    ax.legend(fontsize=11)
    ax.set_xlabel("Umur")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

    # =====================================================
    # GENDER
    # =====================================================
    st.subheader("Distribusi Gender")
    distribusi_gender = df['Gender'].value_counts()
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(distribusi_gender, labels=distribusi_gender.index, autopct='%1.1f%%', wedgeprops=dict(width=0.5), textprops={'fontsize': 13})
    plt.tight_layout()
    st.pyplot(fig)
    
    # =====================================================
    # EDUCATIONN LEVEL
    # =====================================================
    COLORS = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3', '#937860']
    distribusi_education = df['Education_Level'].value_counts()
    st.subheader("Distribusi Tingkat Pendidikan")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(distribusi_education.index, distribusi_education.values, color=COLORS, edgecolor='white')
    ax.set_xlabel('Jumlah Nasabah', fontsize=12)
    ax.set_ylabel('Tingkat Pendidikan', fontsize=12)
    for i, v in enumerate(distribusi_education.values):
        ax.text(v + 30, i, str(v), va='center', fontsize=10)

    st.pyplot(fig)

# =========================================================
# TAB 2
# =========================================================
elif menu == "Perhitungan SAW":
    st.subheader("Bobot Kriteria")

    # Input Bobot
    weights = []
    cols = st.columns(len(CRITERIA_LABELS))
    
    for i, label in enumerate(CRITERIA_LABELS):
        with cols[i]:
            w = st.slider(
                label,
                0.0,
                1.0,
                float(DEFAULT_WEIGHTS[i]),
                0.01
            )
            weights.append(w)

    total_weight = sum(weights)
    st.write(f"Total Bobot = {total_weight:.2f}")
    
    if abs(total_weight - 1.0) > 0.01:
        st.warning("Total bobot sebaiknya = 1.0 untuk hasil yang akurat.")

    # Input Parameter Sampling & Ranking
    col_param1, col_param2 = st.columns(2)
    with col_param1:
        sample_n = st.number_input(
            "Jumlah Data Sampel",
            min_value=50,
            max_value=len(df),
            value=min(500, len(df))
        )
    with col_param2:
        top_n = st.number_input(
            "Jumlah Top Ranking",
            min_value=5,
            max_value=50,
            value=10
        )

    weight_df = pd.DataFrame({
        "Kriteria": CRITERIA_LABELS,
        "Bobot": weights,
        "Jenis": [
            "Benefit" if x == 1 else "Cost"
            for x in CRITERIA_TYPE
        ]
    })

    st.dataframe(weight_df, use_container_width=True)

    if abs(total_weight - 1.0) > 0.01:
        st.warning("Total bobot sebaiknya = 1")

    run_saw = st.button("Hitung SAW")
    if run_saw:
        df_sample = df.sample(
            n=int(sample_n),
            random_state=42
        ).copy()
        x = df_sample[CRITERIA_COLS].values.astype(float)
        m, n = x.shape
        r = np.zeros((m, n))

        # =================================================
        # NORMALISASI
        # =================================================
        for i in range(n):

            if CRITERIA_TYPE[i] == 1:
                r[:, i] = x[:, i] / np.max(x[:, i])

            else:
                r[:, i] = np.min(x[:, i]) / x[:, i]

        # =================================================
        # HITUNG NILAI PREFERENSI
        # =================================================
        w = np.array(weights)
        w = w / np.sum(w)

        v = np.sum(w * r, axis=1)

        df_sample['Skor_SAW'] = v

        df_result = df_sample[
            ['CLIENTNUM', 'Skor_SAW'] + CRITERIA_COLS
        ].sort_values(
            'Skor_SAW',
            ascending=False
        ).reset_index(drop=True)

        df_result.insert(
            0,
            'Peringkat',
            range(1, len(df_result)+1)
        )

        st.session_state['df_result'] = df_result

        st.success("Perhitungan SAW berhasil dilakukan")

    # =====================================================
    # HASIL
    # =====================================================
    if 'df_result' in st.session_state:

        df_result = st.session_state['df_result']

        st.subheader(f"Top {top_n} Ranking Nasabah")

        st.dataframe(
            df_result.head(top_n),
            use_container_width=True
        )

        # =================================================
        # BAR CHART
        # =================================================
        st.subheader(f"Visualisasi Top {top_n} Skor SAW dari {sample_n} sample")

        top_data = df_result.head(top_n)

        fig, ax = plt.subplots(figsize=(10,4))

        ax.bar(
            top_data['Peringkat'].astype(str),
            top_data['Skor_SAW']
        )

        ax.set_xlabel("Peringkat")
        ax.set_ylabel("Skor SAW")

        st.pyplot(fig)

# =========================================================
# TAB 3
# =========================================================
elif menu == "Visualisasi":

    st.subheader("Heatmap Korelasi")

    fig, ax = plt.subplots(figsize=(10,6))

    corr = df[CRITERIA_COLS].corr()

    sns.heatmap(
        corr,
        annot=True,
        cmap='Blues',
        ax=ax
    )

    st.pyplot(fig)

    # =====================================================
    # SCATTER
    # =====================================================
    st.subheader("Credit Limit vs Total Transaction")

    fig, ax = plt.subplots(figsize=(10,5))

    scatter = ax.scatter(
        df['Credit_Limit'],
        df['Total_Trans_Amt'],
        c=df['Avg_Utilization_Ratio'],
        cmap='viridis'
    )

    plt.colorbar(scatter)

    ax.set_xlabel("Credit Limit")
    ax.set_ylabel("Total Transaction Amount")

    st.pyplot(fig)

    # =====================================================
    # DISTRIBUSI SKOR SAW
    # =====================================================
    if 'df_result' in st.session_state:

        df_result = st.session_state['df_result']

        fig, axes = plt.subplots(1, 2, figsize=(14,5))
        st.subheader("Distribusi Skor SAW Semua Nasabah")

        # =====================================================
        # HISTOGRAM
        # =====================================================

        counts, bins, patches = axes[0].hist(
            df_result['Skor_SAW'],
            bins=40,
            edgecolor='white'
        )

        # Warna gradasi biru
        colors = plt.cm.Blues(
            np.linspace(0.4, 0.9, len(patches))
        )

        for color, patch in zip(colors, patches):
            patch.set_facecolor(color)

        axes[0].set_title("Histogram Skor SAW")

        axes[0].set_xlabel("Skor SAW")
        axes[0].set_ylabel("Frekuensi")

        axes[0].grid(axis='y', alpha=0.3)

        # =====================================================
        # SCATTER PLOT
        # =====================================================

        scatter_colors = plt.cm.tab20(
            np.linspace(0, 1, len(df_result))
        )

        axes[1].scatter(
            df_result['Peringkat'],
            df_result['Skor_SAW'],
            color='#2563eb'
        )

        axes[1].set_title("Skor SAW vs Peringkat")

        axes[1].set_xlabel("Peringkat")
        axes[1].set_ylabel("Skor SAW")

        axes[1].grid(True, alpha=0.3)

        axes[1].invert_xaxis()

        # =====================================================
        # SHOW
        # =====================================================

        plt.tight_layout()

        st.pyplot(fig)

        plt.close()

# =========================================================
# TAB 4
# =========================================================
elif menu == "Profil Kelompok":
        st.subheader("Profil Kelompok")
        
        # Data Anggota
        anggota_data = [
            {
                "Nama": "Vincentius Gavrila Subagyo",
                "NIM": "123240146",
                "Peran": "Data Analyst / SPK Analyst"
            },
            {
                "Nama": "Sebastian Alvaro Huller",
                "NIM": "123240162",
                "Peran": "UI Designer / Frontend"
            }
        ]

        # Membuat layout kolom untuk setiap anggota
        cols = st.columns(len(anggota_data))
        
        for i, anggota in enumerate(anggota_data):
            with cols[i]:
                # Menggunakan container dengan border untuk efek kartu
                with st.container(border=True):
                    st.markdown(f"### {anggota['Nama']}")
                    st.markdown(f"**NIM:** {anggota['NIM']}")
                    st.markdown(f"**Peran:** {anggota['Peran']}")
                    # Opsional: Tambahkan ikon atau foto jika ada
                    # st.image("path_to_image.jpg", use_column_width=True) 

        st.divider() # Garis pemisah

        st.subheader("Tentang Proyek")
        st.write("""
        Sistem Pendukung Keputusan (SPK) ini dibuat menggunakan metode
        Simple Additive Weighting (SAW) untuk menentukan nasabah prioritas
        kartu kredit berdasarkan beberapa kriteria.
        """)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "SPK Nasabah Kartu Kredit • Metode SAW • Praktikum SCPK 2025/2026"
)
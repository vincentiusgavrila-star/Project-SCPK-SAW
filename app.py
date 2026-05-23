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
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("BankChurners.csv")
    except:
        np.random.seed(42)

        n = 500

        df = pd.DataFrame({
            'CLIENTNUM': np.arange(700000000, 700000000+n),
            'Attrition_Flag': np.random.choice(
                ['Existing Customer', 'Attrited Customer'],
                n,
                p=[0.84, 0.16]
            ),
            'Customer_Age': np.random.randint(26, 73, n),
            'Gender': np.random.choice(['M', 'F'], n),
            'Education_Level': np.random.choice([
                'Graduate',
                'High School',
                'College',
                'Unknown'
            ], n),
            'Income_Category': np.random.choice([
                'Less than $40K',
                '$40K - $60K',
                '$60K - $80K',
                '$80K - $120K',
                '$120K +'
            ], n),
            'Credit_Limit': np.random.uniform(1000, 35000, n),
            'Total_Trans_Amt': np.random.randint(500, 18000, n),
            'Total_Trans_Ct': np.random.randint(10, 140, n),
            'Months_on_book': np.random.randint(13, 56, n),
            'Avg_Utilization_Ratio': np.random.uniform(0, 1, n),
            'Total_Relationship_Count': np.random.randint(1, 6, n),
            'Contacts_Count_12_mon': np.random.randint(0, 6, n),
            'Months_Inactive_12_mon': np.random.randint(0, 6, n),
        })

    return df

df_raw = load_data()

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
st.title("💳 Sistem Pendukung Keputusan Nasabah Kartu Kredit")
st.write("Metode Simple Additive Weighting (SAW)")

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("⚙️ Pengaturan Bobot")

weights = []

for i, label in enumerate(CRITERIA_LABELS):
    w = st.sidebar.slider(
        label,
        0.0,
        1.0,
        float(DEFAULT_WEIGHTS[i]),
        0.01
    )
    weights.append(w)

total_weight = sum(weights)

st.sidebar.write(f"### Total Bobot = {total_weight:.2f}")

top_n = st.sidebar.number_input(
    "Jumlah Top Ranking",
    5,
    50,
    10
)

sample_n = st.sidebar.number_input(
    "Jumlah Data Sampel",
    50,
    len(df_raw),
    min(500, len(df_raw))
)

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dataset",
    "⚙️ Perhitungan SAW",
    "📈 Visualisasi",
    "👥 Profil Kelompok"
])

# =========================================================
# TAB 1
# =========================================================
with tab1:

    st.subheader("Informasi Dataset")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Jumlah Data", len(df_raw))

    with col2:
        st.metric("Jumlah Kolom", len(df_raw.columns))

    with col3:
        st.metric("Jumlah Kriteria", len(CRITERIA_COLS))

    st.subheader("Dataset")

    st.dataframe(df_raw.head(100), use_container_width=True)

    st.subheader("Statistik Deskriptif")

    st.dataframe(
        df_raw[CRITERIA_COLS].describe(),
        use_container_width=True
    )

    # =====================================================
    # PIE CHART
    # =====================================================
    st.subheader("Distribusi Status Nasabah")

    fig, ax = plt.subplots()

    vals = df_raw['Attrition_Flag'].value_counts()

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

    ax.hist(
        df_raw['Customer_Age'],
        bins=20
    )

    ax.set_xlabel("Umur")
    ax.set_ylabel("Jumlah")

    st.pyplot(fig)

    # =====================================================
    # GENDER
    # =====================================================
    st.subheader("Distribusi Gender")

    fig, ax = plt.subplots()

    gender = df_raw['Gender'].value_counts()

    ax.bar(
        gender.index,
        gender.values
    )

    ax.set_xlabel("Gender")
    ax.set_ylabel("Jumlah")

    st.pyplot(fig)

# =========================================================
# TAB 2
# =========================================================
with tab2:

    st.subheader("Bobot Kriteria")

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

        df_sample = df_raw.sample(
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
        st.subheader("Visualisasi Skor SAW")

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
with tab3:

    st.subheader("Heatmap Korelasi")

    fig, ax = plt.subplots(figsize=(10,6))

    corr = df_raw[CRITERIA_COLS].corr()

    sns.heatmap(
        corr,
        annot=True,
        cmap='Blues',
        ax=ax
    )

    st.pyplot(fig)

    # =====================================================
    # BOXPLOT
    # =====================================================
    st.subheader("Boxplot Kriteria")

    fig, ax = plt.subplots(figsize=(12,5))

    df_raw[CRITERIA_COLS].boxplot(ax=ax)

    plt.xticks(rotation=20)

    st.pyplot(fig)

    # =====================================================
    # SCATTER
    # =====================================================
    st.subheader("Credit Limit vs Total Transaction")

    fig, ax = plt.subplots(figsize=(10,5))

    scatter = ax.scatter(
        df_raw['Credit_Limit'],
        df_raw['Total_Trans_Amt'],
        c=df_raw['Avg_Utilization_Ratio'],
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

        st.subheader("Distribusi Skor SAW")

        fig, ax = plt.subplots(figsize=(10,4))

        ax.hist(
            df_result['Skor_SAW'],
            bins=20
        )

        ax.set_xlabel("Skor")
        ax.set_ylabel("Frekuensi")

        st.pyplot(fig)

# =========================================================
# TAB 4
# =========================================================
with tab4:

    st.subheader("Profil Kelompok")

    anggota = pd.DataFrame({
        "Nama": [
            "Vincentius Gavrila Subagyo",
            "Sebastian Alvaro Huller"
        ],
        "NIM": [
            "123240146",
            "1232401620"
        ],
        "Peran": [
            "Rusher",
            "Libero"
        ]
    })

    st.table(anggota)

    st.subheader("Tentang Proyek")

    st.write("""
    Sistem Pendukung Keputusan (SPK) ini dibuat menggunakan metode
    Simple Additive Weighting (SAW) untuk menentukan nasabah prioritas
    kartu kredit berdasarkan beberapa kriteria.
    """)

    st.subheader("Rumus SAW")

    st.latex(r"r_{ij} = \frac{x_{ij}}{max(x_{ij})}")

    st.latex(r"r_{ij} = \frac{min(x_{ij})}{x_{ij}}")

    st.latex(r"V_i = \sum w_j r_{ij}")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "SPK Nasabah Kartu Kredit • Metode SAW • Praktikum SCPK 2025/2026"
)
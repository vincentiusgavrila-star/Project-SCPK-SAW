import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="SPK Nasabah Kartu Kredit",
    page_icon="💳",
    layout="wide"
)

# ============================================================
# BANKING THEME CSS
# Palette:
#   Navy      #0A2463  (kepercayaan, institusi)
#   Royal     #1E4DB7  (primary action)
#   Gold      #C9A84C  (premium, kartu kredit)
#   Amber     #F0A500  (highlight, active)
#   Emerald   #10805C  (positif, retained)
#   Crimson   #C0392B  (attrition / churn)
#   Slate     #F0F4F8  (background)
#   Card bg   #FFFFFF
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

/* ---- Base ---- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #F0F4F8;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2463 0%, #0D2F7A 60%, #0E3580 100%);
    border-right: 3px solid #C9A84C;
}

[data-testid="stSidebar"] .stRadio label {
    color: #E8EDF5 !important;
    font-size: 0.92rem;
    padding: 6px 4px;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #C9A84C !important;
    font-family: 'Playfair Display', serif;
    letter-spacing: 0.5px;
}

/* ---- Page title ---- */
h1 {
    color: #0A2463 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
    border-bottom: 3px solid #C9A84C;
    padding-bottom: 0.4rem;
}

h2, h3 {
    color: #0A2463 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
}

/* ---- Metric cards ---- */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0A2463 0%, #1E4DB7 100%);
    border: 1px solid #C9A84C;
    border-radius: 12px;
    padding: 16px !important;
    box-shadow: 0 4px 12px rgba(10,36,99,0.18);
}

[data-testid="metric-container"] label {
    color: #C9A84C !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* ---- Buttons ---- */
.stButton button {
    border-radius: 8px;
    background: linear-gradient(135deg, #0A2463 0%, #1E4DB7 100%);
    color: white;
    border: 1px solid #C9A84C;
    font-weight: 600;
    letter-spacing: 0.5px;
    padding: 0.45rem 1.2rem;
    transition: all 0.2s ease;
}

.stButton button:hover {
    background: linear-gradient(135deg, #C9A84C 0%, #F0A500 100%);
    color: #0A2463;
    border-color: #0A2463;
}

/* ---- Dataframe ---- */
[data-testid="stDataFrame"] {
    border: 1px solid #C9A84C33;
    border-radius: 10px;
    overflow: hidden;
}

/* ---- Sliders ---- */
[data-testid="stSlider"] .st-bk {
    background-color: #1E4DB7 !important;
}

/* ---- Info / warning banners ---- */
.stInfo {
    background-color: #EEF2FF;
    border-left: 4px solid #1E4DB7;
    border-radius: 6px;
}

.stSuccess {
    background-color: #ECFDF5;
    border-left: 4px solid #10805C;
}

.stWarning {
    background-color: #FFFBEB;
    border-left: 4px solid #F0A500;
}

/* ---- Forms ---- */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #C9A84C55;
    border-radius: 12px;
    padding: 1.5rem !important;
    box-shadow: 0 2px 8px rgba(10,36,99,0.08);
}

/* ---- Container cards ---- */
[data-testid="stContainer"] {
    border-radius: 12px !important;
}

/* ---- Divider ---- */
hr {
    border-color: #C9A84C55 !important;
    border-width: 1.5px !important;
}

/* ---- Caption / footer ---- */
.stCaption {
    color: #64748B !important;
}

/* ---- Section header badge ---- */
.section-badge {
    display: inline-block;
    background: linear-gradient(135deg, #C9A84C, #F0A500);
    color: #0A2463;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 6px;
}

/* ---- Hero banner ---- */
.hero-banner {
    background: linear-gradient(135deg, #0A2463 0%, #1E4DB7 60%, #0D2F7A 100%);
    border-radius: 14px;
    padding: 1.6rem 2rem;
    color: white;
    margin-bottom: 1.4rem;
    border: 1px solid #C9A84C55;
    box-shadow: 0 6px 24px rgba(10,36,99,0.18);
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: "💳";
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.12;
}

.hero-banner h2 {
    color: #C9A84C !important;
    font-family: 'Playfair Display', serif !important;
    margin: 0 0 6px 0 !important;
    font-size: 1.4rem !important;
}

.hero-banner p {
    color: #BFD0F0;
    margin: 0;
    font-size: 0.88rem;
}

/* ---- Profile cards ---- */
.profile-card {
    background: linear-gradient(160deg, #0A2463 0%, #1E4DB7 100%);
    border-radius: 14px;
    padding: 1.6rem;
    color: white;
    border: 1px solid #C9A84C;
    box-shadow: 0 6px 20px rgba(10,36,99,0.2);
    text-align: center;
}

.profile-card h3 {
    color: #C9A84C !important;
    font-size: 1.05rem !important;
    margin-bottom: 8px !important;
}

.profile-card p {
    color: #BFD0F0;
    font-size: 0.85rem;
    margin: 4px 0;
}

.profile-card .role-badge {
    display: inline-block;
    background: rgba(201,168,76,0.2);
    border: 1px solid #C9A84C;
    color: #F0A500;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 12px;
    border-radius: 20px;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# BANKING MATPLOTLIB THEME
# ============================================================
NAVY       = "#0A2463"
ROYAL      = "#1E4DB7"
GOLD       = "#C9A84C"
AMBER      = "#F0A500"
EMERALD    = "#10805C"
CRIMSON    = "#C0392B"
LIGHT_BLUE = "#BFD0F0"
SLATE      = "#64748B"

def bank_palette(n=8):
    """Return n colors from a banking-themed palette."""
    base = [NAVY, ROYAL, GOLD, EMERALD, CRIMSON, AMBER, "#2980B9", "#8E44AD"]
    return base[:n]

plt.rcParams.update({
    "axes.facecolor":    "#F8FAFF",
    "figure.facecolor":  "#F8FAFF",
    "axes.edgecolor":    "#CBD5E1",
    "axes.linewidth":    0.8,
    "axes.grid":         True,
    "grid.color":        "#E2E8F0",
    "grid.linewidth":    0.6,
    "xtick.color":       SLATE,
    "ytick.color":       SLATE,
    "text.color":        NAVY,
    "axes.labelcolor":   NAVY,
    "axes.titlecolor":   NAVY,
    "axes.titleweight":  "bold",
    "axes.titlesize":    12,
    "font.family":       "sans-serif",
})


# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv("BankChurners.csv")

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

CRITERIA_TYPE    = [1, 1, 1, 1, 0, 1, 0, 0]
DEFAULT_WEIGHTS  = [0.20, 0.25, 0.15, 0.10, 0.10, 0.10, 0.05, 0.05]


# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="hero-banner">
    <h2>Sistem Pendukung Keputusan</h2>
    <p>Nasabah Kartu Kredit &nbsp;•&nbsp; Metode Simple Additive Weighting (SAW)</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("## 💳 Menu Navigasi")
menu = st.sidebar.radio(
    "",
    ["Dataset", "Perhitungan SAW", "Visualisasi", "Profil Kelompok"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small style='color:#8FADD4;'>SCPK 2025/2026</small>",
    unsafe_allow_html=True
)


# ============================================================
# TAB 1 — DATASET
# ============================================================
if menu == "Dataset":

    st.markdown('<span class="section-badge">Overview</span>', unsafe_allow_html=True)
    st.subheader("Informasi Dataset")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jumlah Data", f"{len(df):,}")
    with col2:
        st.metric("Jumlah Kolom", len(df.columns))
    with col3:
        st.metric("Jumlah Kriteria", len(CRITERIA_COLS))

    st.markdown('<span class="section-badge">Data</span>', unsafe_allow_html=True)
    st.subheader("Dataset")
    st.dataframe(df.head(100), use_container_width=True)

    st.markdown('<span class="section-badge">Statistics</span>', unsafe_allow_html=True)
    st.subheader("Statistik Deskriptif")
    st.dataframe(df[CRITERIA_COLS].describe(), use_container_width=True)

    st.markdown('<span class="section-badge">Dashboard</span>', unsafe_allow_html=True)
    st.subheader("Dashboard Visualisasi Dataset")

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.patch.set_facecolor("#F0F4F8")

    # ---- Pie: Attrition ----
    vals   = df['Attrition_Flag'].value_counts()
    colors_pie1 = [EMERALD, CRIMSON]
    wedges, texts, autotexts = axes[0, 0].pie(
        vals,
        labels=vals.index,
        autopct='%1.1f%%',
        colors=colors_pie1,
        startangle=90,
        textprops={'fontsize': 10, 'color': 'white'},
        wedgeprops=dict(edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
    axes[0, 0].set_title("Status Nasabah", fontsize=13, fontweight='bold', color=NAVY, pad=12)
    legend_elements = [
        mpatches.Patch(facecolor=EMERALD, label='Retained'),
        mpatches.Patch(facecolor=CRIMSON, label='Attrited (Churn)'),
    ]
    axes[0, 0].legend(handles=legend_elements, loc='lower center',
                      bbox_to_anchor=(0.5, -0.12), fontsize=9, frameon=False)

    # ---- Histogram: Umur ----
    counts, bins, patches2 = axes[0, 1].hist(
        df['Customer_Age'], bins=20, edgecolor='white', zorder=2
    )
    cmap = plt.cm.Blues
    norm_v = counts / counts.max()
    for patch, nv in zip(patches2, norm_v):
        patch.set_facecolor(cmap(0.35 + 0.55 * nv))
    mean_age = df['Customer_Age'].mean()
    axes[0, 1].axvline(mean_age, color=GOLD, linestyle='--', linewidth=2.2,
                       label=f'Rata-rata: {mean_age:.0f} th', zorder=3)
    axes[0, 1].set_title("Distribusi Umur Nasabah", fontsize=13)
    axes[0, 1].set_xlabel("Umur")
    axes[0, 1].set_ylabel("Jumlah Nasabah")
    axes[0, 1].legend(frameon=True, facecolor='white', edgecolor=GOLD)

    # ---- Donut: Gender ----
    dist_gender = df['Gender'].value_counts()
    colors_g    = [ROYAL, GOLD]
    axes[1, 0].pie(
        dist_gender,
        labels=dist_gender.index,
        autopct='%1.1f%%',
        colors=colors_g,
        wedgeprops=dict(width=0.48, edgecolor='white', linewidth=2),
        startangle=90,
        textprops={'fontsize': 10}
    )
    axes[1, 0].set_title("Distribusi Gender", fontsize=13)

    # ---- Bar H: Pendidikan ----
    dist_edu = df['Education_Level'].value_counts()
    bar_colors = [NAVY, ROYAL, "#2980B9", "#5BA4CF", "#8FADD4",
                  GOLD, AMBER][:len(dist_edu)]
    bars = axes[1, 1].barh(
        dist_edu.index, dist_edu.values,
        color=bar_colors, edgecolor='white', height=0.65
    )
    axes[1, 1].set_title("Distribusi Tingkat Pendidikan", fontsize=13)
    axes[1, 1].set_xlabel("Jumlah Nasabah")
    for i, v in enumerate(dist_edu.values):
        axes[1, 1].text(v + 30, i, str(v), va='center', fontsize=9, color=NAVY)
    axes[1, 1].invert_yaxis()

    plt.tight_layout(pad=2.5)
    st.pyplot(fig)


# ============================================================
# TAB 2 — PERHITUNGAN SAW
# ============================================================
elif menu == "Perhitungan SAW":

    st.markdown('<span class="section-badge">Bobot</span>', unsafe_allow_html=True)
    st.subheader("Bobot Kriteria")

    weights = []
    cols = st.columns(len(CRITERIA_LABELS))
    for i, label in enumerate(CRITERIA_LABELS):
        with cols[i]:
            w = st.slider(label,
                          min_value=0.0, max_value=1.0,
                          value=float(DEFAULT_WEIGHTS[i]),
                          step=0.01, key=f"weight_{i}")
            weights.append(w)

    total_weight = sum(weights)
    if abs(total_weight - 1.0) <= 0.01:
        st.success(f"✅ Total Bobot = **{total_weight:.2f}** — Valid")
    else:
        st.warning(f"⚠️ Total Bobot = **{total_weight:.2f}** — Sebaiknya = 1.00")

    col1, col2 = st.columns(2)
    with col1:
        sample_n = st.number_input("Jumlah Data Sampel",
                                   min_value=50, max_value=len(df),
                                   value=min(500, len(df)))
    with col2:
        top_n = st.number_input("Jumlah Top Ranking",
                                min_value=5, max_value=50, value=10)

    weight_df = pd.DataFrame({
        "Kriteria": CRITERIA_LABELS,
        "Bobot": [f"{w:.2f}" for w in weights],
        "Jenis": ["✅ Benefit" if x == 1 else "❌ Cost" for x in CRITERIA_TYPE]
    })
    st.dataframe(weight_df, use_container_width=True)

    st.divider()

    # ---- Input Alternatif ----
    st.markdown('<span class="section-badge">Input</span>', unsafe_allow_html=True)
    st.subheader("Input Alternatif Baru")

    with st.form("form_alternatif"):
        nama_alternatif = st.text_input("Nama Nasabah", key="nama_nasabah")
        st.info("ℹ️ Masukkan nilai sesuai rentang data yang tersedia.")
        input_data = {}
        for col, label in zip(CRITERIA_COLS, CRITERIA_LABELS):
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            input_data[col] = st.number_input(
                label, min_value=min_val, max_value=max_val,
                value=min_val, key=f"input_{col}"
            )
        submit_alternatif = st.form_submit_button("➕ Tambah Alternatif")

    if submit_alternatif:
        if nama_alternatif.strip() == "":
            st.error("❌ Nama nasabah wajib diisi.")
        else:
            alternatif_baru = {"CLIENTNUM": nama_alternatif}
            for k, v in input_data.items():
                alternatif_baru[k] = v
            st.session_state["alternatif_baru"] = alternatif_baru
            st.success("✅ Alternatif berhasil ditambahkan.")

    if "alternatif_baru" in st.session_state:
        st.subheader("Alternatif Saat Ini")
        st.dataframe(pd.DataFrame([st.session_state["alternatif_baru"]]),
                     use_container_width=True)
        if st.button("🗑️ Hapus Alternatif"):
            del st.session_state["alternatif_baru"]
            st.rerun()

    st.divider()

    # ---- Hitung SAW ----
    run_saw = st.button("⚙️ Hitung SAW", use_container_width=True)

    if run_saw:
        df_sample = df.sample(n=int(sample_n), random_state=42).copy()

        if "alternatif_baru" in st.session_state:
            alternatif_df = pd.DataFrame([st.session_state["alternatif_baru"]])
            df_sample = pd.concat([df_sample, alternatif_df], ignore_index=True)

        x   = df_sample[CRITERIA_COLS].values.astype(float)
        m, n = x.shape
        r   = np.zeros((m, n))

        for i in range(n):
            if CRITERIA_TYPE[i] == 1:
                r[:, i] = x[:, i] / np.max(x[:, i])
            else:
                r[:, i] = np.min(x[:, i]) / x[:, i]

        w = np.array(weights)
        w = w / np.sum(w)
        v = np.sum(w * r, axis=1)

        df_sample["Skor_SAW"] = v
        df_result = (
            df_sample[["CLIENTNUM", "Skor_SAW"] + CRITERIA_COLS]
            .sort_values("Skor_SAW", ascending=False)
            .reset_index(drop=True)
        )
        df_result.insert(0, "Peringkat", range(1, len(df_result) + 1))
        st.session_state["df_result"] = df_result
        st.success("✅ Perhitungan SAW berhasil!")

    # ---- Hasil ----
    if "df_result" in st.session_state:
        df_result = st.session_state["df_result"]

        st.markdown('<span class="section-badge">Hasil</span>', unsafe_allow_html=True)
        st.subheader(f"Top {top_n} Ranking Nasabah")
        st.dataframe(df_result.head(int(top_n)), use_container_width=True)

        if "alternatif_baru" in st.session_state:
            nama = st.session_state["alternatif_baru"]["CLIENTNUM"]
            hasil_user = df_result[df_result["CLIENTNUM"] == nama]
            if len(hasil_user) > 0:
                st.subheader("📌 Peringkat Alternatif yang Ditambahkan")
                st.dataframe(hasil_user, use_container_width=True)

        st.subheader(f"Visualisasi Top {int(top_n)}")
        top_data   = df_result.head(int(top_n))
        n_bars     = len(top_data)
        bar_colors = [
            GOLD if i == 0 else (AMBER if i == 1 else (ROYAL if i == 2 else NAVY))
            for i in range(n_bars)
        ]

        fig, ax = plt.subplots(figsize=(11, 4))
        bars = ax.bar(
            top_data["Peringkat"].astype(str),
            top_data["Skor_SAW"],
            color=bar_colors,
            edgecolor="white",
            width=0.65,
            zorder=2
        )

        # Medal labels on top 3
        for i, (bar, score) in enumerate(
            zip(bars, top_data["Skor_SAW"])
        ):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else ""
            ax.text(bar.get_x() + bar.get_width() / 2,
                    score + 0.003,
                    f"{medal}\n{score:.4f}",
                    ha='center', va='bottom',
                    fontsize=8.5, color=NAVY, fontweight='bold')

        ax.set_xlabel("Peringkat", labelpad=8)
        ax.set_ylabel("Skor SAW")
        ax.set_title("Top Ranking Nasabah — Skor SAW")
        ax.set_ylim(0, top_data["Skor_SAW"].max() * 1.15)

        # Gold accent line on y=0
        ax.axhline(0, color=GOLD, linewidth=1.2)
        plt.tight_layout()
        st.pyplot(fig)


# ============================================================
# TAB 3 — VISUALISASI
# ============================================================
elif menu == "Visualisasi":

    st.markdown('<span class="section-badge">Korelasi</span>', unsafe_allow_html=True)
    st.subheader("Heatmap Korelasi Kriteria")

    fig, ax = plt.subplots(figsize=(11, 6))
    corr = df[CRITERIA_COLS].corr()
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    cmap_custom = sns.diverging_palette(220, 30, as_cmap=True)
    sns.heatmap(
        corr, annot=True, fmt=".2f",
        cmap=cmap_custom,
        ax=ax, linewidths=0.5,
        linecolor="#E2E8F0",
        annot_kws={"size": 9},
        cbar_kws={"shrink": 0.8}
    )
    ax.set_title("Korelasi Antar Kriteria SAW", pad=14)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown('<span class="section-badge">Scatter</span>', unsafe_allow_html=True)
    st.subheader("Credit Limit vs Total Transaction Amount")

    fig, ax = plt.subplots(figsize=(11, 5))
    scatter = ax.scatter(
        df['Credit_Limit'],
        df['Total_Trans_Amt'],
        c=df['Avg_Utilization_Ratio'],
        cmap='RdYlGn_r',
        alpha=0.55,
        s=18,
        edgecolors='none'
    )
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Avg Utilization Ratio", color=NAVY)
    ax.set_xlabel("Credit Limit")
    ax.set_ylabel("Total Transaction Amount")
    ax.set_title("Credit Limit vs Transaction Amount\n(warna = Avg Utilization Ratio)")
    plt.tight_layout()
    st.pyplot(fig)

    if 'df_result' in st.session_state:
        df_result = st.session_state['df_result']

        st.markdown('<span class="section-badge">SAW Distribution</span>',
                    unsafe_allow_html=True)
        st.subheader("Distribusi Skor SAW")

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Histogram
        counts, bins, patches3 = axes[0].hist(
            df_result['Skor_SAW'], bins=40, edgecolor='white', zorder=2
        )
        norm_v2 = counts / counts.max()
        cmap2 = plt.cm.Blues
        for patch, nv in zip(patches3, norm_v2):
            patch.set_facecolor(cmap2(0.3 + 0.65 * nv))

        # Vertical lines: mean & median
        mean_s   = df_result['Skor_SAW'].mean()
        median_s = df_result['Skor_SAW'].median()
        axes[0].axvline(mean_s,   color=GOLD,    linestyle='--', lw=2,
                        label=f'Mean: {mean_s:.4f}')
        axes[0].axvline(median_s, color=CRIMSON,  linestyle=':',  lw=2,
                        label=f'Median: {median_s:.4f}')
        axes[0].set_title("Histogram Skor SAW")
        axes[0].set_xlabel("Skor SAW")
        axes[0].set_ylabel("Frekuensi")
        axes[0].legend(frameon=True, facecolor='white', edgecolor=GOLD, fontsize=9)

        # Scatter rank vs score
        total = len(df_result)
        rank_colors = [
            GOLD   if r <= 3          else
            AMBER  if r <= int(total * 0.1) else
            ROYAL  if r <= int(total * 0.5) else
            CRIMSON
            for r in df_result['Peringkat']
        ]
        axes[1].scatter(
            df_result['Peringkat'],
            df_result['Skor_SAW'],
            c=rank_colors, s=18, alpha=0.7, edgecolors='none', zorder=2
        )
        axes[1].set_title("Skor SAW vs Peringkat")
        axes[1].set_xlabel("Peringkat")
        axes[1].set_ylabel("Skor SAW")
        axes[1].invert_xaxis()

        # Legend
        legend_els = [
            mpatches.Patch(color=GOLD,    label='Top 3 (Emas)'),
            mpatches.Patch(color=AMBER,   label='Top 10%'),
            mpatches.Patch(color=ROYAL,   label='Top 50%'),
            mpatches.Patch(color=CRIMSON, label='Bottom 50%'),
        ]
        axes[1].legend(handles=legend_els, frameon=True,
                       facecolor='white', edgecolor=GOLD, fontsize=8)

        plt.tight_layout(pad=2.5)
        st.pyplot(fig)


# ============================================================
# TAB 4 — PROFIL KELOMPOK
# ============================================================
elif menu == "Profil Kelompok":

    st.markdown('<span class="section-badge">Tim</span>', unsafe_allow_html=True)
    st.subheader("Profil Kelompok")

    anggota_data = [
        {
            "Nama":  "Vincentius Gavrila Subagyo",
            "NIM":   "123240146",
            "Peran": "Data Analyst / SPK Analyst"
        },
        {
            "Nama":  "Sebastian Alvaro Huller",
            "NIM":   "123240162",
            "Peran": "UI Designer / Frontend"
        }
    ]

    cols = st.columns(len(anggota_data))
    for i, anggota in enumerate(anggota_data):
        with cols[i]:
            st.markdown(f"""
            <div class="profile-card">
                <h3>{anggota['Nama']}</h3>
                <p><strong style="color:#C9A84C;">NIM</strong> &nbsp; {anggota['NIM']}</p>
                <div class="role-badge">{anggota['Peran']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<span class="section-badge">Tentang</span>', unsafe_allow_html=True)
    st.subheader("Tentang Proyek")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.write("""
        Sistem Pendukung Keputusan (SPK) ini dibuat menggunakan metode
        **Simple Additive Weighting (SAW)** untuk menentukan nasabah prioritas
        kartu kredit berdasarkan delapan kriteria utama — mulai dari limit kredit,
        frekuensi transaksi, hingga rasio utilisasi.
        """)
        st.write("""
        Data bersumber dari dataset **BankChurners** yang memuat lebih dari
        10.000 rekaman nasabah aktif maupun yang telah *churn*. SPK ini membantu
        analis memperoleh ranking nasabah secara objektif dan terukur.
        """)
    with col2:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{NAVY},{ROYAL});
                    border-radius:12px; padding:1.2rem; border:1px solid {GOLD};
                    color:white; text-align:center;">
            <p style="color:{GOLD}; font-weight:700; font-size:0.75rem;
                       letter-spacing:1px; text-transform:uppercase; margin:0 0 8px 0;">
                Stack Teknologi
            </p>
            <p style="margin:4px 0; font-size:0.88rem;">🐍 Python</p>
            <p style="margin:4px 0; font-size:0.88rem;">📊 Streamlit</p>
            <p style="margin:4px 0; font-size:0.88rem;">🔢 NumPy · Pandas</p>
            <p style="margin:4px 0; font-size:0.88rem;">📈 Matplotlib · Seaborn</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("💳  SPK Nasabah Kartu Kredit  •  Metode SAW  •  Praktikum SCPK 2025/2026")
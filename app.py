import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SPK Nasabah Kartu Kredit",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  GLOBAL STYLE INJECTION
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Syne:wght@700;800&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Hide default Streamlit header */
header[data-testid="stHeader"] { background: transparent; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29, #302b63, #24243e);
    border-right: 2px solid #a78bfa44;
}
[data-testid="stSidebar"] * { color: #e2d9f3 !important; }
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label { color: #c4b5fd !important; font-weight: 600; }

/* Main background */
.main .block-container {
    background: #0d0d1a;
    padding: 2rem 2.5rem;
    border-radius: 0;
}

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
    border: 1px solid #533483;
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, #7c3aed22 0%, transparent 60%),
                radial-gradient(circle at 70% 50%, #2563eb22 0%, transparent 60%);
    pointer-events: none;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0; line-height: 1.1;
}
.hero p { color: #94a3b8; font-size: 1.05rem; margin-top: 0.6rem; }

/* Metric cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 160px;
    border-radius: 16px; padding: 1.2rem 1.5rem;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}
.metric-card.purple { background: linear-gradient(135deg, #4c1d95cc, #7c3aedcc); }
.metric-card.blue   { background: linear-gradient(135deg, #1e3a5fcc, #2563ebcc); }
.metric-card.green  { background: linear-gradient(135deg, #064e3bcc, #059669cc); }
.metric-card.orange { background: linear-gradient(135deg, #78350fcc, #d97706cc); }
.metric-card.pink   { background: linear-gradient(135deg, #831843cc, #ec4899cc); }
.metric-num { font-family:'Syne',sans-serif; font-size:2rem; font-weight:800; color:#fff; }
.metric-label { color: rgba(255,255,255,0.7); font-size:0.82rem; margin-top:0.2rem; }

/* Section titles */
.section-title {
    font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 700;
    color: #e2d9f3; margin: 1.5rem 0 1rem; display: flex; align-items: center; gap: 0.6rem;
}
.tag {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 1px; vertical-align: middle;
}
.tag-purple { background: #7c3aed33; color: #a78bfa; border: 1px solid #7c3aed66; }
.tag-green  { background: #05966933; color: #34d399; border: 1px solid #05966966; }
.tag-blue   { background: #2563eb33; color: #60a5fa; border: 1px solid #2563eb66; }

/* Rank badge */
.rank-1 { color: #fbbf24; font-weight: 800; }
.rank-2 { color: #94a3b8; font-weight: 800; }
.rank-3 { color: #f97316; font-weight: 800; }

/* Divider */
.fancy-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #7c3aed, #2563eb, #059669, transparent);
    border: none; margin: 2rem 0;
}

/* Tab override */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1a2e; border-radius: 12px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #94a3b8;
    border-radius: 8px; font-weight: 600; padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
}

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid #7c3aed44; border-radius: 12px; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    padding: 0.65rem 2rem !important; font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px #7c3aed44 !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px #7c3aed66 !important;
}

/* General text */
p, li, span, label { color: #cbd5e1; }
h2, h3 { color: #e2d9f3; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MATPLOTLIB DARK THEME
# ─────────────────────────────────────────────
PALETTE = ["#a78bfa","#60a5fa","#34d399","#fb923c","#f472b6","#facc15","#38bdf8","#4ade80"]
plt.rcParams.update({
    'figure.facecolor': '#0d0d1a',
    'axes.facecolor':   '#131325',
    'axes.edgecolor':   '#2d2d4e',
    'axes.labelcolor':  '#94a3b8',
    'xtick.color':      '#64748b',
    'ytick.color':      '#64748b',
    'text.color':       '#e2d9f3',
    'grid.color':       '#1e1e3a',
    'grid.linestyle':   '--',
    'grid.alpha':       0.5,
    'font.family':      'DejaVu Sans',
    'axes.titlecolor':  '#e2d9f3',
})

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="⚡ Memuat dataset...")
def load_data():
    try:
        df=pd.read_csv('BankChurners.csv')
    except Exception:
        # fallback: random synthetic data for demo
        np.random.seed(42)
        n = 300
        df = pd.DataFrame({
            'CLIENTNUM': np.arange(700000000, 700000000+n),
            'Attrition_Flag': np.random.choice(['Existing Customer','Attrited Customer'], n, p=[0.84,0.16]),
            'Customer_Age': np.random.randint(26, 73, n),
            'Gender': np.random.choice(['M','F'], n, p=[0.47,0.53]),
            'Education_Level': np.random.choice(['Graduate','High School','Unknown','Uneducated','College','Post-Graduate','Doctorate'], n),
            'Income_Category': np.random.choice(['Less than $40K','$40K - $60K','$60K - $80K','$80K - $120K','$120K +','Unknown'], n),
            'Credit_Limit': np.random.uniform(1438, 34516, n),
            'Total_Trans_Amt': np.random.randint(510, 18484, n),
            'Total_Trans_Ct': np.random.randint(10, 139, n),
            'Months_on_book': np.random.randint(13, 56, n),
            'Avg_Utilization_Ratio': np.random.uniform(0, 0.999, n),
            'Total_Relationship_Count': np.random.randint(1, 6, n),
            'Contacts_Count_12_mon': np.random.randint(0, 6, n),
            'Months_Inactive_12_mon': np.random.randint(0, 6, n),
        })
    return df

df_raw = load_data()

CRITERIA_COLS = [
    'Credit_Limit', 'Total_Trans_Amt', 'Total_Trans_Ct',
    'Months_on_book', 'Avg_Utilization_Ratio',
    'Total_Relationship_Count', 'Contacts_Count_12_mon',
    'Months_Inactive_12_mon'
]
CRITERIA_LABELS = [
    'Credit Limit', 'Total Trans Amt', 'Total Trans Ct',
    'Months on Book', 'Avg Util Ratio',
    'Rel. Count', 'Contacts (12M)', 'Inactive (12M)'
]
CRITERIA_TYPE = [1,1,1,1,0,1,0,0]   # 1=benefit, 0=cost
DEFAULT_WEIGHTS = [0.20,0.25,0.15,0.10,0.10,0.10,0.05,0.05]

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:1rem 0'>"
                "<span style='font-family:Syne,sans-serif;font-size:1.6rem;font-weight:800;"
                "background:linear-gradient(90deg,#a78bfa,#60a5fa);-webkit-background-clip:text;"
                "-webkit-text-fill-color:transparent'>💳 SPK SAW</span>"
                "<p style='color:#64748b;font-size:0.78rem;margin:0'>Sistem Pendukung Keputusan</p>"
                "</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Bobot Kriteria")
    st.caption("Total bobot harus = 1.0")

    weights = []
    weight_names = [
        ("💰","Credit Limit"),("💸","Total Trans Amt"),("🔢","Total Trans Ct"),
        ("📅","Months on Book"),("📊","Avg Util Ratio"),("🤝","Rel. Count"),
        ("📞","Contacts (12M)"),("💤","Inactive (12M)"),
    ]
    for i,(icon,name) in enumerate(weight_names):
        w = st.slider(f"{icon} {name}", 0.0, 1.0, float(DEFAULT_WEIGHTS[i]), 0.01, key=f"w{i}")
        weights.append(w)

    total_w = sum(weights)
    color = "#34d399" if abs(total_w-1.0)<0.01 else "#f87171"
    st.markdown(f"<div style='text-align:center;padding:0.6rem;border-radius:10px;"
                f"background:#1a1a2e;border:1px solid {color}33;margin-top:0.5rem'>"
                f"<span style='color:{color};font-weight:700;font-size:1.1rem'>Σ = {total_w:.2f}</span></div>",
                unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Filter Tampilan")
    top_n = st.number_input("Top-N Nasabah Ditampilkan", min_value=5, max_value=100, value=10, step=5)
    sample_n = st.number_input("Jumlah Sampel Dihitung", min_value=50, max_value=len(df_raw),
                                value=min(500, len(df_raw)), step=50)

# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class='hero'>
  <h1>💳 Sistem Pendukung Keputusan<br>Nasabah Kartu Kredit</h1>
  <p>Metode Simple Additive Weighting (SAW) • Dataset: Credit Card Customers • Kaggle</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dataset & EDA",
    "⚙️ Hitung SPK",
    "📈 Visualisasi Analitik",
    "👥 Profil Kelompok"
])

# ══════════════════════════════════════════════
#  TAB 1 – DATASET & EDA
# ══════════════════════════════════════════════
with tab1:
    # Quick stats
    col1,col2,col3,col4,col5 = st.columns(5)
    stats_data = [
        ("purple","💳",f"{len(df_raw):,}","Total Nasabah"),
        ("blue","📋",str(len(df_raw.columns)),"Jumlah Kolom"),
        ("green","✅",f"{df_raw.isnull().sum().sum()}","Missing Values"),
        ("orange","📈",f"{len(CRITERIA_COLS)}","Kriteria SAW"),
        ("pink","🏆","SAW","Metode SPK"),
    ]
    for col,(clr,icon,num,lbl) in zip([col1,col2,col3,col4,col5],stats_data):
        with col:
            st.markdown(f"""<div class='metric-card {clr}'>
                <div class='metric-num'>{icon} {num}</div>
                <div class='metric-label'>{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📋 Dataset Mentah <span class='tag tag-purple'>RAW DATA</span></div>",
                unsafe_allow_html=True)
    st.dataframe(df_raw.head(100), use_container_width=True, height=320)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔬 Statistik Deskriptif <span class='tag tag-blue'>DESCRIBE</span></div>",
                unsafe_allow_html=True)
    st.dataframe(df_raw[CRITERIA_COLS].describe().round(3), use_container_width=True)

    # ── EDA Charts ──────────────────────────────
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Exploratory Data Analysis</div>", unsafe_allow_html=True)

    # Row 1: Pie charts
    c1,c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6,5))
        vals = df_raw['Attrition_Flag'].value_counts()
        clrs = ["#7c3aed","#f472b6"]
        wedges,_,autos = ax.pie(vals, labels=vals.index, autopct='%1.1f%%',
                                 colors=clrs, startangle=140,
                                 wedgeprops=dict(width=0.6, edgecolor='#0d0d1a', linewidth=2),
                                 textprops={'fontsize':11,'color':'#e2d9f3'})
        for a in autos: a.set_color('#fff'); a.set_fontweight('bold')
        ax.set_title("Status Nasabah (Attrition Flag)", fontsize=13, fontweight='bold', pad=12)
        centre = plt.Circle((0,0),0.38,color='#131325')
        ax.add_artist(centre)
        ax.text(0,0,f"{len(df_raw):,}\nNasabah",ha='center',va='center',color='#e2d9f3',
                fontsize=10,fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with c2:
        fig, ax = plt.subplots(figsize=(6,5))
        vals = df_raw['Gender'].value_counts()
        clrs2 = ["#60a5fa","#fb923c"]
        wedges,_,autos = ax.pie(vals, labels=vals.index, autopct='%1.1f%%',
                                 colors=clrs2, startangle=90,
                                 wedgeprops=dict(width=0.55, edgecolor='#0d0d1a', linewidth=2),
                                 textprops={'fontsize':12,'color':'#e2d9f3'})
        for a in autos: a.set_color('#fff'); a.set_fontweight('bold')
        ax.set_title("Distribusi Jenis Kelamin", fontsize=13, fontweight='bold', pad=12)
        centre = plt.Circle((0,0),0.36,color='#131325')
        ax.add_artist(centre)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    # Row 2: Age histogram
    fig, ax = plt.subplots(figsize=(12,4))
    n_bins = 25
    counts, bin_edges = np.histogram(df_raw['Customer_Age'], bins=n_bins)
    colors_grad = plt.cm.plasma(np.linspace(0.2,0.9,n_bins))
    for i in range(n_bins):
        ax.bar(bin_edges[i], counts[i], width=(bin_edges[1]-bin_edges[0])*0.85,
               color=colors_grad[i], align='edge', edgecolor='none', alpha=0.9)
    ax.axvline(df_raw['Customer_Age'].mean(), color='#34d399', linestyle='--', linewidth=2,
               label=f"Rata-rata: {df_raw['Customer_Age'].mean():.1f} thn")
    ax.set_title("Distribusi Usia Nasabah", fontsize=14, fontweight='bold')
    ax.set_xlabel("Usia (Tahun)"); ax.set_ylabel("Jumlah Nasabah")
    ax.legend(fontsize=11); ax.grid(axis='y')
    ax.set_facecolor('#131325')
    plt.tight_layout(); st.pyplot(fig); plt.close()

    # Row 3: Education + Income
    c3,c4 = st.columns(2)
    with c3:
        fig, ax = plt.subplots(figsize=(6.5,4.5))
        edu = df_raw['Education_Level'].value_counts()
        bars = ax.barh(edu.index, edu.values,
                       color=PALETTE[:len(edu)], edgecolor='none', height=0.65)
        for bar,val in zip(bars, edu.values):
            ax.text(bar.get_width()+30, bar.get_y()+bar.get_height()/2,
                    str(val), va='center', fontsize=9, color='#94a3b8')
        ax.set_title("Tingkat Pendidikan Nasabah", fontsize=13, fontweight='bold')
        ax.set_xlabel("Jumlah Nasabah"); ax.grid(axis='x')
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with c4:
        fig, ax = plt.subplots(figsize=(6.5,4.5))
        order = ['Less than $40K','$40K - $60K','$60K - $80K','$80K - $120K','$120K +','Unknown']
        inc = df_raw['Income_Category'].value_counts().reindex(order).fillna(0).astype(int)
        bars = ax.bar(inc.index, inc.values,
                      color=PALETTE[:len(inc)], edgecolor='none', width=0.65)
        for bar,val in zip(bars, inc.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
                    str(val), ha='center', fontsize=9, color='#94a3b8')
        ax.set_title("Kategori Pendapatan Nasabah", fontsize=13, fontweight='bold')
        ax.set_xlabel("Kategori"); ax.set_ylabel("Jumlah"); ax.tick_params(axis='x',rotation=20)
        ax.grid(axis='y')
        plt.tight_layout(); st.pyplot(fig); plt.close()

# ══════════════════════════════════════════════
#  TAB 2 – HITUNG SPK
# ══════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-title'>⚙️ Konfigurasi SAW <span class='tag tag-blue'>SETUP</span></div>",
                unsafe_allow_html=True)

    # Show weight summary
    w_df = pd.DataFrame({
        "Kriteria": CRITERIA_LABELS,
        "Jenis": ["Benefit" if t==1 else "Cost" for t in CRITERIA_TYPE],
        "Bobot": [round(w,3) for w in weights]
    })
    c_left, c_right = st.columns([1,1])
    with c_left:
        st.dataframe(w_df, use_container_width=True, hide_index=True)
    with c_right:
        fig, ax = plt.subplots(figsize=(5,4))
        clrs_type = ["#60a5fa" if t==1 else "#f87171" for t in CRITERIA_TYPE]
        bars = ax.barh(CRITERIA_LABELS, weights, color=clrs_type, edgecolor='none', height=0.6)
        for bar,w in zip(bars,weights):
            ax.text(bar.get_width()+0.003, bar.get_y()+bar.get_height()/2,
                    f"{w:.2f}", va='center', fontsize=9, color='#e2d9f3')
        ax.set_xlim(0, max(weights)*1.25)
        ax.set_title("Distribusi Bobot Kriteria", fontsize=12, fontweight='bold')
        blue_p = mpatches.Patch(color='#60a5fa', label='Benefit')
        red_p  = mpatches.Patch(color='#f87171', label='Cost')
        ax.legend(handles=[blue_p,red_p], fontsize=9, loc='lower right')
        plt.tight_layout(); st.pyplot(fig); plt.close()

    if abs(sum(weights)-1.0) > 0.01:
        st.warning("⚠️ Total bobot belum = 1.0! Silakan sesuaikan slider di Sidebar.")

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)

    # Trigger button
    col_btn = st.columns([1,2,1])
    with col_btn[1]:
        run_saw = st.button("🚀 Jalankan Perhitungan SAW", use_container_width=True)

    if run_saw:
        if abs(sum(weights)-1.0) > 0.05:
            st.error("Total bobot terlalu jauh dari 1.0! Harap sesuaikan terlebih dahulu.")
            st.stop()

        with st.spinner("⚡ Menghitung SAW..."):
            df_sample = df_raw.sample(n=int(sample_n), random_state=42).copy()

            x = df_sample[CRITERIA_COLS].values.astype(float)
            eps = 1e-10
            m, n_c = x.shape
            r = np.zeros((m, n_c))

            for i in range(n_c):
                if CRITERIA_TYPE[i] == 1:
                    r[:,i] = x[:,i] / (np.max(x[:,i]) + eps)
                else:
                    r[:,i] = np.min(x[:,i]) / (x[:,i] + eps)

            w_arr = np.array(weights)
            w_arr = w_arr / w_arr.sum()
            v = np.sum(w_arr * r, axis=1)

            df_sample['Skor_SAW'] = v
            df_result = df_sample[['CLIENTNUM','Skor_SAW'] + CRITERIA_COLS] \
                            .sort_values('Skor_SAW', ascending=False).reset_index(drop=True)
            df_result.insert(0, 'Peringkat', range(1, len(df_result)+1))

            st.session_state['df_result'] = df_result

        st.success(f"✅ Perhitungan SAW selesai! {len(df_result):,} nasabah berhasil diperingkat.")

    if 'df_result' in st.session_state:
        df_result = st.session_state['df_result']
        st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'>🏆 Tabel Perangkingan Nasabah "
                    f"<span class='tag tag-green'>TOP {top_n}</span></div>", unsafe_allow_html=True)

        # Top-3 highlight
        medals = ["🥇","🥈","🥉"]
        top3_cols = st.columns(3)
        for i, col in enumerate(top3_cols):
            row = df_result.iloc[i]
            with col:
                st.markdown(f"""<div class='metric-card {"purple" if i==0 else "blue" if i==1 else "orange"}'>
                    <div style='font-size:2rem'>{medals[i]}</div>
                    <div class='metric-num' style='font-size:1.3rem'>#{row['Peringkat']}</div>
                    <div class='metric-label'>{int(row['CLIENTNUM'])}</div>
                    <div style='color:#fff;font-weight:700;font-size:1.1rem'>Skor: {row['Skor_SAW']:.4f}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        display_cols = ['Peringkat','CLIENTNUM','Skor_SAW','Credit_Limit',
                        'Total_Trans_Amt','Total_Trans_Ct','Avg_Utilization_Ratio']
        st.dataframe(
            df_result[display_cols].head(int(top_n)).style
                .background_gradient(subset=['Skor_SAW'], cmap='plasma')
                .format({'Skor_SAW':'{:.4f}','Credit_Limit':'{:,.0f}',
                         'Total_Trans_Amt':'{:,.0f}','Avg_Utilization_Ratio':'{:.3f}'}),
            use_container_width=True, hide_index=True
        )

        # Bar chart result
        st.markdown("<div class='section-title'>📊 Visualisasi Skor SAW Top Nasabah</div>",
                    unsafe_allow_html=True)
        top_n_data = df_result.head(int(top_n))
        fig, ax = plt.subplots(figsize=(14, 5))
        grad_colors = plt.cm.plasma(np.linspace(0.85, 0.2, len(top_n_data)))
        bars = ax.bar(range(len(top_n_data)), top_n_data['Skor_SAW'],
                      color=grad_colors, edgecolor='none', width=0.75)
        ax.set_xticks(range(len(top_n_data)))
        ax.set_xticklabels([f"#{r}" for r in top_n_data['Peringkat']], fontsize=10)
        for bar,score in zip(bars, top_n_data['Skor_SAW']):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.002,
                    f"{score:.4f}", ha='center', fontsize=8, color='#94a3b8')
        ax.set_title(f"Skor SAW Top {top_n} Nasabah Prioritas", fontsize=14, fontweight='bold')
        ax.set_xlabel("Peringkat"); ax.set_ylabel("Skor SAW")
        ax.grid(axis='y'); plt.tight_layout()
        st.pyplot(fig); plt.close()

# ══════════════════════════════════════════════
#  TAB 3 – VISUALISASI ANALITIK
# ══════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-title'>📈 Visualisasi Analitik Lengkap "
                "<span class='tag tag-purple'>SAW • ANALITIK</span></div>", unsafe_allow_html=True)

    if 'df_result' not in st.session_state:
        st.info("💡 Jalankan perhitungan SAW di tab **⚙️ Hitung SPK** terlebih dahulu untuk melihat semua visualisasi.")
        st.markdown("*(Visualisasi EDA tetap tersedia di bawah)*")

    # ── Viz 1: Correlation Heatmap ─────────────
    st.markdown("<div class='section-title'>🔥 Heatmap Korelasi Antar Kriteria</div>",
                unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12,7))
    corr = df_raw[CRITERIA_COLS].corr()
    mask = np.triu(np.ones_like(corr), k=1)
    cmap = sns.diverging_palette(240, 10, as_cmap=True)
    sns.heatmap(corr, annot=True, fmt='.2f', cmap=cmap, center=0,
                ax=ax, linewidths=0.5, linecolor='#0d0d1a',
                cbar_kws={'shrink':0.8}, annot_kws={'size':10})
    ax.set_xticklabels(CRITERIA_LABELS, rotation=30, ha='right', fontsize=9)
    ax.set_yticklabels(CRITERIA_LABELS, rotation=0, fontsize=9)
    ax.set_title("Korelasi Antar Kriteria SAW", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout(); st.pyplot(fig); plt.close()

    # ── Viz 2: Boxplots per criteria ─────────────
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📦 Distribusi Setiap Kriteria (Boxplot)</div>",
                unsafe_allow_html=True)
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    for i, (col, label) in enumerate(zip(CRITERIA_COLS, CRITERIA_LABELS)):
        data = df_raw[col].dropna()
        bp = axes[i].boxplot(data, patch_artist=True, notch=True,
                             boxprops=dict(facecolor=PALETTE[i]+'88', color=PALETTE[i]),
                             medianprops=dict(color='#fff', linewidth=2),
                             whiskerprops=dict(color=PALETTE[i]),
                             capprops=dict(color=PALETTE[i]),
                             flierprops=dict(marker='o', color=PALETTE[i], alpha=0.3, markersize=3))
        axes[i].set_title(label, fontsize=10, fontweight='bold', color=PALETTE[i])
        axes[i].grid(axis='y', alpha=0.4)
        t_label = "✅ Benefit" if CRITERIA_TYPE[i]==1 else "🔴 Cost"
        axes[i].text(1.25, np.median(data), t_label, va='center', fontsize=8, color='#94a3b8')
    plt.suptitle("Distribusi Nilai Setiap Kriteria", fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout(); st.pyplot(fig); plt.close()

    # ── Viz 3: Score distribution (if SAW ran) ─────
    if 'df_result' in st.session_state:
        df_result = st.session_state['df_result']
        st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🎯 Distribusi Skor SAW Semua Nasabah</div>",
                    unsafe_allow_html=True)
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Histogram
        counts, bins, patches = axes[0].hist(df_result['Skor_SAW'], bins=40, edgecolor='none')
        cm = plt.cm.plasma
        bin_centers = 0.5*(bins[:-1]+bins[1:])
        col_norm = (bin_centers - bin_centers.min()) / (bin_centers.max() - bin_centers.min())
        for c, p in zip(col_norm, patches): p.set_facecolor(cm(c))
        axes[0].set_title("Histogram Skor SAW", fontsize=13, fontweight='bold')
        axes[0].set_xlabel("Skor SAW"); axes[0].set_ylabel("Frekuensi")
        axes[0].grid(axis='y')
        # Add percentile lines
        for pct, col, lbl in [(25,'#60a5fa','Q1'),(50,'#34d399','Median'),(75,'#fb923c','Q3')]:
            val = np.percentile(df_result['Skor_SAW'], pct)
            axes[0].axvline(val, color=col, linestyle='--', linewidth=1.5, label=f"{lbl}: {val:.4f}")
        axes[0].legend(fontsize=9)

        # Scatter: rank vs score
        scatter_c = plt.cm.cool(np.linspace(0, 1, len(df_result)))
        axes[1].scatter(df_result['Peringkat'], df_result['Skor_SAW'],
                        c=scatter_c, s=12, alpha=0.7, edgecolors='none')
        axes[1].set_title("Skor SAW vs Peringkat", fontsize=13, fontweight='bold')
        axes[1].set_xlabel("Peringkat"); axes[1].set_ylabel("Skor SAW")
        axes[1].grid(True, alpha=0.3)
        axes[1].invert_xaxis()

        plt.tight_layout(); st.pyplot(fig); plt.close()

        # ── Viz 4: Radar for Top 5 ─────────────
        st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🕸️ Radar Chart — Profil Top 5 Nasabah</div>",
                    unsafe_allow_html=True)

        top5 = df_result.head(5)
        categories = CRITERIA_LABELS
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)] + [0]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.set_facecolor('#131325')
        radar_colors = ["#a78bfa","#60a5fa","#34d399","#fb923c","#f472b6"]
        for idx, (_, row) in enumerate(top5.iterrows()):
            vals = []
            for col, ctype in zip(CRITERIA_COLS, CRITERIA_TYPE):
                mx = df_raw[col].max()
                mn = df_raw[col].min()
                norm = (row[col]-mn)/(mx-mn+1e-10)
                if ctype == 0: norm = 1 - norm
                vals.append(norm)
            vals += [vals[0]]
            ax.plot(angles, vals, 'o-', linewidth=2,
                    color=radar_colors[idx], label=f"#{int(row['Peringkat'])} | {int(row['CLIENTNUM'])}")
            ax.fill(angles, vals, alpha=0.12, color=radar_colors[idx])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=9, color='#94a3b8')
        ax.set_ylim(0,1); ax.set_yticks([0.25,0.5,0.75,1.0])
        ax.set_yticklabels(['0.25','0.50','0.75','1.00'], fontsize=7, color='#4a4a6a')
        ax.grid(color='#2d2d4e', linestyle='--', alpha=0.7)
        ax.set_title("Profil Kriteria Top 5 Nasabah", fontsize=14, fontweight='bold',
                     pad=20, color='#e2d9f3')
        ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=9)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        # ── Viz 5: Stacked contribution ─────────
        st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📊 Kontribusi Bobot Tiap Kriteria (Stacked Bar)</div>",
                    unsafe_allow_html=True)

        top10_radar = df_result.head(int(top_n))
        w_arr = np.array(weights); w_arr = w_arr/w_arr.sum()
        contrib_data = {}
        for col, label, ctype, w in zip(CRITERIA_COLS, CRITERIA_LABELS, CRITERIA_TYPE, w_arr):
            eps2=1e-10
            if ctype==1:
                contrib = (top10_radar[col] / (df_raw[col].max()+eps2)) * w
            else:
                contrib = (df_raw[col].min() / (top10_radar[col]+eps2)) * w
            contrib_data[label] = contrib.values

        contrib_df = pd.DataFrame(contrib_data,
                                  index=[f"#{r}" for r in top10_radar['Peringkat']])
        fig, ax = plt.subplots(figsize=(14,6))
        bottom = np.zeros(len(contrib_df))
        for i, col in enumerate(contrib_df.columns):
            ax.bar(contrib_df.index, contrib_df[col], bottom=bottom,
                   color=PALETTE[i % len(PALETTE)], label=col, edgecolor='none', width=0.7)
            bottom += contrib_df[col].values
        ax.set_title(f"Kontribusi Kriteria per Nasabah (Top {top_n})", fontsize=13, fontweight='bold')
        ax.set_xlabel("Peringkat Nasabah"); ax.set_ylabel("Kontribusi Skor")
        ax.legend(loc='upper right', fontsize=8, ncol=2)
        ax.grid(axis='y', alpha=0.4); plt.tight_layout()
        st.pyplot(fig); plt.close()

    # ── Viz 6: Credit Limit vs Trans Amt scatter ─
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💡 Credit Limit vs Total Transaksi</div>",
                unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12,5))
    sample_viz = df_raw.sample(min(1000, len(df_raw)), random_state=1)
    sc = ax.scatter(sample_viz['Credit_Limit'], sample_viz['Total_Trans_Amt'],
                    c=sample_viz['Avg_Utilization_Ratio'], cmap='plasma',
                    alpha=0.6, s=20, edgecolors='none')
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Avg Utilization Ratio", color='#94a3b8')
    ax.set_xlabel("Credit Limit"); ax.set_ylabel("Total Transaction Amount")
    ax.set_title("Credit Limit vs Total Transaksi (warna = Utilization Ratio)",
                 fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3); plt.tight_layout(); st.pyplot(fig); plt.close()

# ══════════════════════════════════════════════
#  TAB 4 – PROFIL KELOMPOK
# ══════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class='hero' style='text-align:center'>
      <h1 style='font-size:2rem'>👥 Profil Kelompok</h1>
      <p>Proyek Akhir Praktikum SCPK 2025/2026</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    for col, (num, name, nim, role) in zip([c1,c2],[
        ("01","Nama Anggota 1","NIM 1","Ketua Kelompok"),
        ("02","Nama Anggota 2","NIM 2","Anggota"),
    ]):
        with col:
            st.markdown(f"""
            <div class='metric-card {"purple" if num=="01" else "blue"}' style='text-align:center;padding:2rem'>
                <div style='font-size:3rem'>{'👨‍💻' if num=='01' else '👩‍💻'}</div>
                <div class='metric-num' style='font-size:1.4rem'>{name}</div>
                <div class='metric-label'>{nim}</div>
                <div style='margin-top:0.5rem'>
                    <span class='tag {"tag-purple" if num=="01" else "tag-blue"}'>{role}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#131325;border:1px solid #7c3aed44;border-radius:16px;padding:2rem;'>
        <div class='section-title'>📋 Detail Proyek</div>
        <table style='width:100%;color:#94a3b8;border-collapse:separate;border-spacing:0 8px'>
            <tr><td style='color:#a78bfa;font-weight:600;width:220px'>📌 Judul Proyek</td>
                <td>Sistem Pendukung Keputusan Nasabah Prioritas Kartu Kredit</td></tr>
            <tr><td style='color:#60a5fa;font-weight:600'>🧮 Metode SPK</td>
                <td>Simple Additive Weighting (SAW)</td></tr>
            <tr><td style='color:#34d399;font-weight:600'>📂 Dataset</td>
                <td>Credit Card Customers — Kaggle (sakshigoyal7)</td></tr>
            <tr><td style='color:#fb923c;font-weight:600'>📊 Jumlah Data</td>
                <td>>10.000 baris, 8 kriteria numerik</td></tr>
            <tr><td style='color:#f472b6;font-weight:600'>🏫 Mata Kuliah</td>
                <td>Praktikum SCPK 2025/2026</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#131325;border:1px solid #34d39944;border-radius:16px;padding:1.5rem'>
        <div class='section-title'>📖 Tentang Metode SAW</div>
        <p style='color:#94a3b8;line-height:1.8'>
        <b style='color:#a78bfa'>Simple Additive Weighting (SAW)</b> adalah metode penjumlahan terbobot yang bekerja
        dengan menormalkan nilai setiap kriteria kemudian mengalikannya dengan bobot masing-masing.
        <br><br>
        <b style='color:#60a5fa'>Rumus Normalisasi:</b><br>
        • <span style='color:#34d399'>Benefit</span>: r<sub>ij</sub> = x<sub>ij</sub> / max(x<sub>ij</sub>)<br>
        • <span style='color:#f87171'>Cost</span>: r<sub>ij</sub> = min(x<sub>ij</sub>) / x<sub>ij</sub><br><br>
        <b style='color:#fb923c'>Rumus Nilai Preferensi:</b> V<sub>i</sub> = Σ w<sub>j</sub> × r<sub>ij</sub>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────
st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;padding:1rem 0;color:#4a4a6a;font-size:0.82rem'>
    💳 SPK Nasabah Kartu Kredit &nbsp;•&nbsp; Metode SAW &nbsp;•&nbsp;
    Praktikum SCPK 2025/2026 &nbsp;•&nbsp;
    Built with <span style='color:#f472b6'>♥</span> using Streamlit
</div>
""", unsafe_allow_html=True)

import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px


st.set_page_config(
    page_title="Loblaw Bio",
    layout="wide"
)

col1, col2, col3 = st.columns([1, 6, 4.3])
with col1:
    st.image("logo.png", width=200)
with col2:
    st.title("Loblaw Bio")
with col3:
    st.markdown("""
        <div style="text-align:right; padding-top: 20px;">
            <span style="font-size:13px; color:#888;">Bob Loblaw</span>
            <div style="width:34px; height:34px; border-radius:50%; background:#E8860A; 
                        display:inline-flex; align-items:center; justify-content:center; 
                        color:white; font-size:13px; font-weight:500; margin-left:8px;">BL</div>
        </div>
    """, unsafe_allow_html=True)



st.divider()

@st.cache_resource
def get_connection():
    return sqlite3.connect('cell-count.db', check_same_thread=False)

conn = get_connection()
c = conn.cursor()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Samples", "10,500")
with col2:
    st.metric("Responders", "331")
with col3:
    st.metric("Non-responders", "325")
with col4:
    st.metric("Significant Population", "cd4_t_cell", delta="p = 0.0133")


st.divider()

st.sidebar.markdown("### Navigation")
page = st.sidebar.radio("", ["Immune Changes", "Frequency Summary", "Subset Analysis"])

st.sidebar.divider()
st.sidebar.markdown("**Trial Info**")
st.sidebar.markdown("Drug: miraclib")
st.sidebar.markdown("Condition: melanoma")
st.sidebar.markdown("Sample type: PBMC")

if page == "Immune Changes":
    st.subheader("Cell Population Boxplots")
    st.markdown("""
    <span style="background:#EFF6FF; color:#1D4ED8; font-size:13px; padding:6px 14px; border-radius:99px; display:inline-block;">
        Responders vs Non-responders · PBMC · miraclib · melanoma
    </span>
""", unsafe_allow_html=True)

    c.execute("""
        SELECT sa.b_cell, sa.cd8_t_cell, sa.cd4_t_cell, sa.nk_cell, sa.monocyte, su.response
        FROM samples sa
        JOIN subjects su ON sa.subject = su.subject
        WHERE su.condition = 'melanoma'
        AND su.treatment = 'miraclib'
        AND sa.sample_type = 'PBMC'
        AND su.response IN ('yes', 'no')
    """)
    rows = c.fetchall()

    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    data = []
    for row in rows:
        counts = [row[0], row[1], row[2], row[3], row[4]]
        total = sum(counts)
        response = row[5]
        for i, pop in enumerate(populations):
            pct = (counts[i] / total) * 100
            data.append({'population': pop, 'percentage': pct, 'response': response})

    df = pd.DataFrame(data)
    fig = px.box(df, x='population', y='percentage', color='response',
                title='Cell Population Frequencies: Responders vs Non-Responders',
                labels={'percentage': 'Frequency (%)', 'population': 'Population'},
                color_discrete_map={'yes': '#378ADD', 'no': '#E8860A'})

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend_title='Response'
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "Frequency Summary":
    st.subheader("Frequency Summary")
    st.markdown("""
    <span style="background:#EFF6FF; color:#1D4ED8; font-size:13px; padding:6px 14px; border-radius:99px; display:inline-block;">
        Relative frequency of each immune cell population per sample
    </span><br><br>
""", unsafe_allow_html=True)

    # filters
    col1, col2, col3 = st.columns(3)
    with col1:
        condition = st.selectbox("Condition", ["All", "melanoma", "carcinoma", "healthy"])
    with col2:
        treatment = st.selectbox("Treatment", ["All", "miraclib", "phauximab", "none"])
    with col3:
        timepoint = st.selectbox("Timepoint", ["All", "0", "7", "14"])

    query = """
    SELECT sa.sample_id, su.condition, su.treatment, sa.time_from_treatment_start,
           sa.b_cell, sa.cd8_t_cell, sa.cd4_t_cell, sa.nk_cell, sa.monocyte
    FROM samples sa
    JOIN subjects su ON sa.subject = su.subject
    WHERE 1=1
    """
    if condition != "All":
        query += f" AND su.condition = '{condition}'"
    if treatment != "All":
        query += f" AND su.treatment = '{treatment}'"
    if timepoint != "All":
        query += f" AND sa.time_from_treatment_start = {timepoint}"

    c.execute(query)
    rows = c.fetchall()

    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    data = []
    for row in rows:
        counts = [int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8])]
        total = sum(counts)
        for i, pop in enumerate(populations):
            pct = round((counts[i] / total) * 100, 2)
            data.append({
                'sample': row[0],
                'condition': row[1],
                'treatment': row[2],
                'timepoint': row[3],
                'population': pop,
                'count': counts[i],
                'total_count': total,
                'percentage': pct
            })

    df2 = pd.DataFrame(data)
    st.dataframe(df2, use_container_width=True)

elif page == "Subset Analysis":
    st.subheader("Subset Analysis: Baseline (time = 0)")
    st.info("Melanoma · miraclib · PBMC only")

    col1, col2, col3 = st.columns(3)

    # samples per project
    c.execute("""
        SELECT su.project, COUNT(*) as sample_count
        FROM samples sa
        JOIN subjects su ON sa.subject = su.subject
        WHERE su.condition = 'melanoma'
        AND su.treatment = 'miraclib'
        AND sa.sample_type = 'PBMC'
        AND sa.time_from_treatment_start = 0
        GROUP BY su.project
    """)
    projects = c.fetchall()
    project_str = " · ".join([f"{p[0]}: {p[1]}" for p in projects])

    # responders vs non-responders
    c.execute("""
        SELECT su.response, COUNT(DISTINCT su.subject)
        FROM samples sa
        JOIN subjects su ON sa.subject = su.subject
        WHERE su.condition = 'melanoma'
        AND su.treatment = 'miraclib'
        AND sa.sample_type = 'PBMC'
        AND sa.time_from_treatment_start = 0
        GROUP BY su.response
    """)
    responses = dict(c.fetchall())

    # males vs females
    c.execute("""
        SELECT su.sex, COUNT(DISTINCT su.subject)
        FROM samples sa
        JOIN subjects su ON sa.subject = su.subject
        WHERE su.condition = 'melanoma'
        AND su.treatment = 'miraclib'
        AND sa.sample_type = 'PBMC'
        AND sa.time_from_treatment_start = 0
        GROUP BY su.sex
    """)
    sexes = dict(c.fetchall())

    # avg b_cell
    c.execute("""
        SELECT ROUND(AVG(sa.b_cell), 2)
        FROM samples sa
        JOIN subjects su ON sa.subject = su.subject
        WHERE su.condition = 'melanoma'
        AND su.treatment = 'miraclib'
        AND sa.sample_type = 'PBMC'
        AND sa.time_from_treatment_start = 0
        AND su.sex = 'M'
        AND su.response = 'yes'
    """)
    avg_bcell = c.fetchone()[0]

    with col1:
        st.metric("Samples per Project", project_str)
    with col2:
        st.metric("Responders / Non-responders", f"{responses.get('yes', 0)} / {responses.get('no', 0)}")
    with col3:
        st.metric("Males / Females", f"{sexes.get('M', 0)} / {sexes.get('F', 0)}")

    st.divider()
    st.metric("Avg B-cell count (melanoma male responders, time=0)", avg_bcell)

st.divider()
st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <h3 style="margin:0;">Custom Query</h3>
        <span style="background:#EDE9FE; color:#5B21B6; font-size:12px; padding:4px 12px; border-radius:99px;">Mann-Whitney U · p &lt; 0.05</span>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    sex_filter = st.selectbox("Sex", ["M", "F"])
with col2:
    pop_filter = st.selectbox("Cell Population", ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte'])
with col3:
    time_filter = st.selectbox("Timepoint", [0, 7, 14])

c.execute(f"""
    SELECT ROUND(AVG(sa.{pop_filter}), 2)
    FROM samples sa
    JOIN subjects su ON sa.subject = su.subject
    WHERE su.condition = 'melanoma'
    AND su.treatment = 'miraclib'
    AND sa.sample_type = 'PBMC'
    AND sa.time_from_treatment_start = {time_filter}
    AND su.sex = '{sex_filter}'
    AND su.response = 'yes'
""")
result = c.fetchone()[0]

st.metric(f"Avg {pop_filter} count ({sex_filter} · melanoma · responders · time={time_filter})", result)

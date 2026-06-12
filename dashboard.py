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


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TalentLens AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CORPORATE CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #f0f4f8; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a2463 0%, #1e3a8a 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stRadio label { 
        font-size: 15px !important;
        padding: 8px 0px !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 12px;
        padding: 16px 20px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #1e3a8a;
    }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 13px !important; }
    [data-testid="stMetricValue"] { color: #0a2463 !important; font-size: 28px !important; font-weight: 700 !important; }

    /* Page title */
    h1 { color: #0a2463 !important; font-weight: 800 !important; }
    h2, h3 { color: #1e3a8a !important; font-weight: 600 !important; }

    /* Chart containers */
    [data-testid="stPlotlyChart"] {
        background: white;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    /* Divider */
    hr { border-color: #e2e8f0 !important; }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* Header banner */
    .header-banner {
        background: linear-gradient(135deg, #0a2463 0%, #1e40af 50%, #3b82f6 100%);
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        color: white;
    }
    .header-banner h1 { color: white !important; margin: 0; font-size: 32px; }
    .header-banner p  { color: #bfdbfe !important; margin: 6px 0 0 0; font-size: 15px; }

    /* Section card */
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ── DATABASE ──────────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    return create_engine("mysql+pymysql://root:Admin123@localhost/talentlens")

@st.cache_data
def run_query(query):
    return pd.read_sql(query, get_engine())

# ── CHART TEMPLATE ────────────────────────────────────────────────────────────
CORP = dict(
    template='plotly_white',
    font=dict(family='Inter, sans-serif', size=13, color='#1e293b'),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=40, b=20)
)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🔍 TalentLens AI")
st.sidebar.markdown("*Job Market Intelligence*")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "🏠 Executive Overview",
    "🛠️ Skill Intelligence",
    "💰 Salary Analytics",
    "🏙️ Geographic Insights",
    "🏭 Industry Analysis"
])
st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Dataset:** 123K+ LinkedIn Jobs")
st.sidebar.markdown("🗄️ **Source:** LinkedIn 2024")
st.sidebar.markdown("🛠️ **Stack:** Python · SQL · Streamlit")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Executive Overview":

    st.markdown("""
    <div class="header-banner">
        <h1>🔍 TalentLens AI</h1>
        <p>Real-time job market intelligence from 123,000+ LinkedIn job postings · 2024</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    total_jobs      = run_query("SELECT COUNT(*) AS c FROM jobs")['c'][0]
    total_companies = run_query("SELECT COUNT(DISTINCT company_id) FROM jobs")['COUNT(DISTINCT company_id)'][0]
    remote_pct      = run_query("SELECT ROUND(SUM(is_remote)*100.0/COUNT(*),1) AS r FROM jobs")['r'][0]
    avg_salary      = run_query("SELECT ROUND(AVG(med_salary),0) AS a FROM salaries WHERE med_salary IS NOT NULL")['a'][0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📋 Total Jobs",    f"{total_jobs:,}")
    c2.metric("🏢 Companies",     f"{total_companies:,}")
    c3.metric("🌐 Remote Jobs",   f"{remote_pct}%")
    c4.metric("💰 Avg Salary",    f"${avg_salary:,.0f}")

    st.markdown("---")
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 🛠️ Top 10 In-Demand Skills")
        df = run_query("""
            SELECT s.skill_name, COUNT(js.job_id) AS demand
            FROM job_skills js JOIN skills s ON js.skill_abr = s.skill_abr
            GROUP BY s.skill_name ORDER BY demand DESC LIMIT 10
        """)
        fig = go.Figure(go.Bar(
            x=df['demand'], y=df['skill_name'],
            orientation='h',
            marker=dict(
                color=df['demand'],
                colorscale=[[0,'#93c5fd'],[0.5,'#3b82f6'],[1,'#1e3a8a']],
                showscale=False
            ),
            text=df['demand'].apply(lambda x: f'{x:,}'),
            textposition='outside'
        ))
        fig.update_layout(
            yaxis=dict(categoryorder='total ascending'),
            xaxis_title="Job Postings",
            height=380, **CORP
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🌐 Remote vs Onsite")
        df2 = run_query("""
            SELECT CASE WHEN is_remote=1 THEN 'Remote' ELSE 'Onsite' END AS work_mode,
                   COUNT(*) AS total FROM jobs GROUP BY is_remote
        """)
        fig2 = go.Figure(go.Pie(
            labels=df2['work_mode'],
            values=df2['total'],
            hole=0.55,
            marker_colors=['#1e3a8a','#93c5fd'],
            textinfo='label+percent',
            textfont_size=14
        ))
        fig2.update_layout(height=380, showlegend=True, **CORP)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🏙️ Top Hiring Cities")
        df3 = run_query("""
            SELECT city, COUNT(*) AS job_count FROM jobs
            WHERE city IS NOT NULL AND city != '' AND city != 'United States'
            GROUP BY city ORDER BY job_count DESC LIMIT 8
        """)
        fig3 = go.Figure(go.Bar(
            x=df3['city'], y=df3['job_count'],
            marker=dict(
                color=df3['job_count'],
                colorscale=[[0,'#bfdbfe'],[1,'#1e3a8a']],
                showscale=False
            ),
            text=df3['job_count'].apply(lambda x: f'{x:,}'),
            textposition='outside'
        ))
        fig3.update_layout(xaxis_tickangle=-30, height=340, **CORP)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("### 💰 Salary by Experience")
        df4 = run_query("""
            SELECT j.experience_level, ROUND(AVG(s.med_salary),0) AS avg_salary
            FROM jobs j JOIN salaries s ON j.job_id = s.job_id
            WHERE s.med_salary IS NOT NULL AND j.experience_level != 'Not Specified'
            GROUP BY j.experience_level ORDER BY avg_salary DESC
        """)
        fig4 = go.Figure(go.Bar(
            x=df4['experience_level'], y=df4['avg_salary'],
            marker=dict(
                color=df4['avg_salary'],
                colorscale=[[0,'#bbf7d0'],[0.5,'#22c55e'],[1,'#14532d']],
                showscale=False
            ),
            text=df4['avg_salary'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside'
        ))
        fig4.update_layout(xaxis_tickangle=-20, height=340, **CORP)
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SKILL INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🛠️ Skill Intelligence":
    st.markdown("""
    <div class="header-banner">
        <h1>🛠️ Skill Intelligence</h1>
        <p>Discover the most demanded skills in today's job market</p>
    </div>
    """, unsafe_allow_html=True)

    top_n = st.slider("Number of skills to display", 5, 35, 15)

    df = run_query(f"""
        SELECT s.skill_name, COUNT(js.job_id) AS demand
        FROM job_skills js JOIN skills s ON js.skill_abr = s.skill_abr
        GROUP BY s.skill_name ORDER BY demand DESC LIMIT {top_n}
    """)

    fig = go.Figure(go.Bar(
        x=df['skill_name'], y=df['demand'],
        marker=dict(
            color=df['demand'],
            colorscale=[[0,'#93c5fd'],[0.5,'#3b82f6'],[1,'#1e3a8a']],
            showscale=True,
            colorbar=dict(title="Demand")
        ),
        text=df['demand'].apply(lambda x: f'{x:,}'),
        textposition='outside'
    ))
    fig.update_layout(
        xaxis_tickangle=-30,
        xaxis_title="Skill",
        yaxis_title="Number of Job Postings",
        height=450,
        title=f"Top {top_n} Most Demanded Skills",
        **CORP
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Skills Data Table")
    st.dataframe(df.style.background_gradient(
        subset=['demand'], cmap='Blues'
    ), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SALARY ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰 Salary Analytics":
    st.markdown("""
    <div class="header-banner">
        <h1>💰 Salary Analytics</h1>
        <p>Deep dive into compensation trends across roles and experience levels</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Salary by Experience Level")
        df = run_query("""
            SELECT j.experience_level,
                   ROUND(AVG(s.med_salary),0) AS avg_salary,
                   COUNT(*) AS job_count
            FROM jobs j JOIN salaries s ON j.job_id = s.job_id
            WHERE s.med_salary IS NOT NULL
            AND j.experience_level != 'Not Specified'
            GROUP BY j.experience_level ORDER BY avg_salary DESC
        """)
        fig = go.Figure(go.Bar(
            x=df['experience_level'], y=df['avg_salary'],
            marker=dict(
                color=df['avg_salary'],
                colorscale=[[0,'#bbf7d0'],[0.5,'#22c55e'],[1,'#14532d']],
                showscale=False
            ),
            text=df['avg_salary'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside'
        ))
        fig.update_layout(height=380, xaxis_tickangle=-15, **CORP)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏆 Top 10 Highest Paying Roles")
        df2 = run_query("""
            SELECT j.title, ROUND(AVG(s.med_salary),0) AS avg_salary,
                   COUNT(*) AS job_count
            FROM jobs j JOIN salaries s ON j.job_id = s.job_id
            WHERE s.med_salary IS NOT NULL AND s.med_salary < 500000
            GROUP BY j.title HAVING job_count >= 5
            ORDER BY avg_salary DESC LIMIT 10
        """)
        fig2 = go.Figure(go.Bar(
            x=df2['avg_salary'], y=df2['title'],
            orientation='h',
            marker=dict(
                color=df2['avg_salary'],
                colorscale=[[0,'#fde68a'],[0.5,'#f59e0b'],[1,'#78350f']],
                showscale=False
            ),
            text=df2['avg_salary'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside'
        ))
        fig2.update_layout(
            yaxis=dict(categoryorder='total ascending'),
            height=380, **CORP
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 Salary Distribution")
    df3 = run_query("""
        SELECT med_salary FROM salaries
        WHERE med_salary IS NOT NULL AND med_salary < 400000
    """)
    fig3 = go.Figure(go.Histogram(
        x=df3['med_salary'], nbinsx=50,
        marker_color='#3b82f6',
        opacity=0.8
    ))
    fig3.update_layout(
        xaxis_title="Salary (USD)",
        yaxis_title="Number of Jobs",
        height=350,
        title="Salary Distribution Across All Jobs",
        **CORP
    )
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — GEOGRAPHIC INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏙️ Geographic Insights":
    st.markdown("""
    <div class="header-banner">
        <h1>🏙️ Geographic Hiring Insights</h1>
        <p>Discover where the jobs are across the United States</p>
    </div>
    """, unsafe_allow_html=True)

    df = run_query("""
        SELECT city, COUNT(*) AS job_count FROM jobs
        WHERE city IS NOT NULL AND city != '' AND city != 'United States'
        GROUP BY city ORDER BY job_count DESC LIMIT 15
    """)

    fig = go.Figure(go.Bar(
        x=df['city'], y=df['job_count'],
        marker=dict(
            color=df['job_count'],
            colorscale=[[0,'#bfdbfe'],[0.5,'#3b82f6'],[1,'#1e3a8a']],
            showscale=True,
            colorbar=dict(title="Jobs")
        ),
        text=df['job_count'].apply(lambda x: f'{x:,}'),
        textposition='outside'
    ))
    fig.update_layout(
        xaxis_tickangle=-30,
        xaxis_title="City",
        yaxis_title="Number of Jobs",
        height=430,
        title="Top 15 Hiring Cities",
        **CORP
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔍 Search Jobs by City")
    city_input = st.text_input("Enter city name (e.g. New York, Chicago, Austin)")
    if city_input:
        df_city = run_query(f"""
            SELECT j.title, j.experience_level,
                   j.work_type_clean, j.is_remote, j.posted_date
            FROM jobs j
            WHERE j.city LIKE '%{city_input}%'
            LIMIT 50
        """)
        st.markdown(f"**Found {len(df_city)} jobs in {city_input}**")
        st.dataframe(df_city, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — INDUSTRY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏭 Industry Analysis":
    st.markdown("""
    <div class="header-banner">
        <h1>🏭 Industry Analysis</h1>
        <p>Understand which industries are hiring the most</p>
    </div>
    """, unsafe_allow_html=True)

    df = run_query("""
        SELECT i.industry_name, COUNT(ji.job_id) AS job_count
        FROM job_industries ji JOIN industries i ON ji.industry_id = i.industry_id
        GROUP BY i.industry_name ORDER BY job_count DESC LIMIT 15
    """)

    col1, col2 = st.columns([3, 2])

    with col1:
        fig = go.Figure(go.Bar(
            x=df['job_count'], y=df['industry_name'],
            orientation='h',
            marker=dict(
                color=df['job_count'],
                colorscale=[[0,'#c4b5fd'],[0.5,'#8b5cf6'],[1,'#4c1d95']],
                showscale=False
            ),
            text=df['job_count'].apply(lambda x: f'{x:,}'),
            textposition='outside'
        ))
        fig.update_layout(
            yaxis=dict(categoryorder='total ascending'),
            xaxis_title="Number of Jobs",
            height=480,
            title="Top 15 Industries by Job Postings",
            **CORP
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure(go.Pie(
            labels=df['industry_name'].head(8),
            values=df['job_count'].head(8),
            hole=0.45,
            textinfo='label+percent',
            textfont_size=11,
            marker=dict(colors=px.colors.qualitative.Bold)
        ))
        fig2.update_layout(
            title="Industry Share (Top 8)",
            height=480,
            showlegend=False,
            **CORP
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📋 Full Industry Table")
    st.dataframe(
        df.style.background_gradient(subset=['job_count'], cmap='Purples'),
        use_container_width=True
    )
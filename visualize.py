import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import mysql.connector
import os

# ── CONNECTION ────────────────────────────────────────────────────────────────
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Admin123', 
    database='talentlens'
)

OUTPUT = r"C:\Users\Dinesh chandra reddy\TalentLens-AI\visualizations"
os.makedirs(OUTPUT, exist_ok=True)

# ── STYLE ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f0f1a',
    'axes.facecolor'  : '#1a1a2e',
    'axes.labelcolor' : 'white',
    'xtick.color'     : 'white',
    'ytick.color'     : 'white',
    'text.color'      : 'white',
    'grid.color'      : '#333355',
    'grid.linestyle'  : '--',
    'grid.alpha'      : 0.5
})

# ── 1. TOP 10 SKILLS ──────────────────────────────────────────────────────────
df1 = pd.read_sql("""
    SELECT s.skill_name, COUNT(js.job_id) AS demand_count
    FROM job_skills js JOIN skills s ON js.skill_abr = s.skill_abr
    GROUP BY s.skill_name ORDER BY demand_count DESC LIMIT 10
""", conn)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(df1['skill_name'], df1['demand_count'],
               color=plt.cm.plasma([i/10 for i in range(10)]))
ax.set_title('Top 10 Most Demanded Skills', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Number of Job Postings')
ax.invert_yaxis()
ax.grid(axis='x')
for bar, val in zip(bars, df1['demand_count']):
    ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/01_top_skills.png", dpi=150)
plt.close()
print("✅ Chart 1 saved — Top Skills")

# ── 2. REMOTE VS ONSITE ───────────────────────────────────────────────────────
df2 = pd.read_sql("""
    SELECT CASE WHEN is_remote=1 THEN 'Remote' ELSE 'Onsite' END AS work_mode,
           COUNT(*) AS total
    FROM jobs GROUP BY is_remote
""", conn)

fig, ax = plt.subplots(figsize=(7, 7))
colors = ['#7b2ff7', '#f72f7b']
wedges, texts, autotexts = ax.pie(
    df2['total'], labels=df2['work_mode'],
    autopct='%1.1f%%', colors=colors,
    startangle=90, pctdistance=0.75,
    wedgeprops=dict(width=0.5)
)
for t in texts + autotexts:
    t.set_color('white')
    t.set_fontsize(13)
ax.set_title('Remote vs Onsite Jobs', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/02_remote_vs_onsite.png", dpi=150)
plt.close()
print("✅ Chart 2 saved — Remote vs Onsite")

# ── 3. TOP 10 HIRING CITIES ───────────────────────────────────────────────────
df3 = pd.read_sql("""
    SELECT city, COUNT(*) AS job_count FROM jobs
    WHERE city IS NOT NULL AND city != '' AND city != 'United States'
    GROUP BY city ORDER BY job_count DESC LIMIT 10
""", conn)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df3['city'], df3['job_count'],
              color=plt.cm.cool([i/10 for i in range(10)]))
ax.set_title('Top 10 Hiring Cities', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Number of Jobs')
ax.tick_params(axis='x', rotation=30)
ax.grid(axis='y')
for bar, val in zip(bars, df3['job_count']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'{val:,}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/03_top_cities.png", dpi=150)
plt.close()
print("✅ Chart 3 saved — Top Cities")

# ── 4. SALARY BY EXPERIENCE ───────────────────────────────────────────────────
df4 = pd.read_sql("""
    SELECT j.experience_level, ROUND(AVG(s.med_salary),0) AS avg_salary
    FROM jobs j JOIN salaries s ON j.job_id = s.job_id
    WHERE s.med_salary IS NOT NULL AND j.experience_level != 'Not Specified'
    GROUP BY j.experience_level ORDER BY avg_salary DESC
""", conn)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df4['experience_level'], df4['avg_salary'],
              color=['#f72f7b','#ff6b35','#f7c948','#7bed9f','#70a1ff','#a29bfe'])
ax.set_title('Average Salary by Experience Level', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Average Salary (USD)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.grid(axis='y')
for bar, val in zip(bars, df4['avg_salary']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
            f'${val:,.0f}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/04_salary_by_experience.png", dpi=150)
plt.close()
print("✅ Chart 4 saved — Salary by Experience")

# ── 5. TOP INDUSTRIES ─────────────────────────────────────────────────────────
df5 = pd.read_sql("""
    SELECT i.industry_name, COUNT(ji.job_id) AS job_count
    FROM job_industries ji JOIN industries i ON ji.industry_id = i.industry_id
    GROUP BY i.industry_name ORDER BY job_count DESC LIMIT 10
""", conn)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(df5['industry_name'], df5['job_count'],
               color=plt.cm.viridis([i/10 for i in range(10)]))
ax.set_title('Top 10 Industries by Hiring', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Number of Jobs')
ax.invert_yaxis()
ax.grid(axis='x')
for bar, val in zip(bars, df5['job_count']):
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/05_top_industries.png", dpi=150)
plt.close()
print("✅ Chart 5 saved — Top Industries")

conn.close()
print(f"\n🎉 All charts saved to {OUTPUT}")
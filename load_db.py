import pandas as pd
import mysql.connector
from mysql.connector import Error

# ── DB CONNECTION ─────────────────────────────────────────────────────────────
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Admin123', 
    database='talentlens'
)
cursor = conn.cursor()
print("✅ Connected to MySQL")

BASE = r"C:\Users\Dinesh chandra reddy\linkedin-job-postings"
CLEANED = r"C:\Users\Dinesh chandra reddy\TalentLens-AI\data\cleaned"

# ── 1. LOAD SKILLS ────────────────────────────────────────────────────────────
print("Loading skills...")
skills = pd.read_csv(f"{BASE}/mappings/skills.csv")
for _, row in skills.iterrows():
    cursor.execute(
        "INSERT IGNORE INTO skills VALUES (%s, %s)",
        (row['skill_abr'], row['skill_name'])
    )
conn.commit()
print(f"  ✅ {len(skills)} skills loaded")

# ── 2. LOAD INDUSTRIES ────────────────────────────────────────────────────────
print("Loading industries...")
industries = pd.read_csv(f"{BASE}/mappings/industries.csv")
for _, row in industries.iterrows():
    if pd.isna(row['industry_name']):
        continue
    cursor.execute(
        "INSERT IGNORE INTO industries VALUES (%s, %s)",
        (int(row['industry_id']), str(row['industry_name']))
    )
conn.commit()
print(f"  ✅ {len(industries)} industries loaded")

# ── 3. LOAD COMPANIES ─────────────────────────────────────────────────────────
print("Loading companies...")
companies = pd.read_csv(f"{BASE}/companies/companies.csv")
comp_ind  = pd.read_csv(f"{BASE}/companies/company_industries.csv")

# Get first industry per company
first_ind = comp_ind.groupby('company_id')['industry'].first().reset_index()
companies = companies.merge(first_ind, on='company_id', how='left')
companies['industry'] = companies['industry'].fillna('Unknown')

for _, row in companies.iterrows():
    cursor.execute(
        "INSERT IGNORE INTO companies VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            int(row['company_id']),
            str(row['name'])[:255],
            int(row['company_size']) if pd.notna(row['company_size']) else None,
            str(row['city'])[:100]    if pd.notna(row['city'])         else None,
            str(row['state'])[:100]   if pd.notna(row['state'])        else None,
            str(row['country'])[:100] if pd.notna(row['country'])      else None,
            str(row['industry'])[:255]
        )
    )
conn.commit()
print(f"  ✅ {len(companies)} companies loaded")

# ── 4. LOAD JOBS ──────────────────────────────────────────────────────────────
print("Loading jobs...")
jobs = pd.read_csv(f"{CLEANED}/jobs_cleaned.csv")

for _, row in jobs.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO jobs VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row['job_id']),
        int(row['company_id'])      if pd.notna(row.get('company_id'))       else None,
        str(row['title'])[:255],
        str(row['location'])[:255],
        str(row['city'])[:100]      if pd.notna(row['city'])                 else None,
        str(row['state'])[:100]     if pd.notna(row['state'])                else None,
        str(row['country'])[:100]   if pd.notna(row['country'])              else None,
        str(row['work_type_clean'])[:50],
        str(row['experience_level'])[:50],
        int(row['is_remote']),
        str(row['posted_date']),
        str(row['posted_month']),
        int(row['posted_year'])     if pd.notna(row['posted_year'])          else None
    ))
conn.commit()
print(f"  ✅ {len(jobs)} jobs loaded")

# ── 5. LOAD SALARIES ──────────────────────────────────────────────────────────
print("Loading salaries...")
salaries = pd.read_csv(f"{BASE}/jobs/salaries.csv")
for _, row in salaries.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO salaries VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row['salary_id']),
        int(row['job_id']),
        float(row['max_salary']) if pd.notna(row['max_salary']) else None,
        float(row['med_salary']) if pd.notna(row['med_salary']) else None,
        float(row['min_salary']) if pd.notna(row['min_salary']) else None,
        str(row['pay_period'])   if pd.notna(row['pay_period']) else None,
        str(row['currency'])     if pd.notna(row['currency'])   else None,
        str(row['compensation_type']) if pd.notna(row['compensation_type']) else None
    ))
conn.commit()
print(f"  ✅ {len(salaries)} salaries loaded")

# ── 6. LOAD JOB SKILLS ────────────────────────────────────────────────────────
print("Loading job_skills...")
job_skills = pd.read_csv(f"{BASE}/jobs/job_skills.csv")
for _, row in job_skills.iterrows():
    cursor.execute(
        "INSERT IGNORE INTO job_skills VALUES (%s, %s)",
        (int(row['job_id']), str(row['skill_abr']))
    )
conn.commit()
print(f"  ✅ {len(job_skills)} job_skills loaded")

# ── 7. LOAD JOB INDUSTRIES ────────────────────────────────────────────────────
print("Loading job_industries...")
job_ind = pd.read_csv(f"{BASE}/jobs/job_industries.csv")
for _, row in job_ind.iterrows():
    cursor.execute(
        "INSERT IGNORE INTO job_industries VALUES (%s, %s)",
        (int(row['job_id']), int(row['industry_id']))
    )
conn.commit()
print(f"  ✅ {len(job_ind)} job_industries loaded")

cursor.close()
conn.close()
print("\n🎉 All data loaded into MySQL successfully!")
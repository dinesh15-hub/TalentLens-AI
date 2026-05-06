import pandas as pd
import numpy as np
import os

print("Loading data...")
df = pd.read_csv(r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\postings.csv")

# ── 1. KEEP ONLY USEFUL COLUMNS ──────────────────────────────────────────────
cols_to_keep = [
    'job_id', 'company_name', 'title', 'location',
    'formatted_work_type', 'formatted_experience_level',
    'min_salary', 'max_salary', 'normalized_salary',
    'pay_period', 'remote_allowed', 'listed_time',
    'work_type', 'description'
]
df = df[cols_to_keep].copy()
print(f"After column selection: {df.shape}")

# ── 2. REMOVE DUPLICATES ─────────────────────────────────────────────────────
df = df.drop_duplicates(subset='job_id')
print(f"After removing duplicates: {df.shape}")

# ── 3. CLEAN COLUMN NAMES ────────────────────────────────────────────────────
df = df.rename(columns={
    'formatted_work_type'       : 'work_type_clean',
    'formatted_experience_level': 'experience_level',
    'listed_time'               : 'posted_timestamp'
})

# ── 4. HANDLE MISSING VALUES ─────────────────────────────────────────────────
df['company_name']    = df['company_name'].fillna('Unknown')
df['experience_level']= df['experience_level'].fillna('Not Specified')
df['remote_allowed']  = df['remote_allowed'].fillna(0)
df['description']     = df['description'].fillna('')

# ── 5. CLEAN LOCATION — extract city, state, country ─────────────────────────
df['city']    = df['location'].str.split(',').str[0].str.strip()
df['state']   = df['location'].str.split(',').str[1].str.strip()
df['country'] = df['location'].str.split(',').str[-1].str.strip()

# ── 6. STANDARDIZE SALARY ────────────────────────────────────────────────────
df['salary'] = df['normalized_salary']
mask = df['salary'].isna()
df.loc[mask, 'salary'] = (
    (df.loc[mask, 'min_salary'] + df.loc[mask, 'max_salary']) / 2
)

# ── 7. CONVERT TIMESTAMPS TO DATES ───────────────────────────────────────────
df['posted_date']  = pd.to_datetime(df['posted_timestamp'], unit='ms', errors='coerce')
df['posted_month'] = df['posted_date'].dt.to_period('M').astype(str)
df['posted_year']  = df['posted_date'].dt.year

# ── 8. CLEAN REMOTE FLAG ─────────────────────────────────────────────────────
df['is_remote'] = df['remote_allowed'].apply(lambda x: 1 if x == 1.0 else 0)

# ── 9. DROP REDUNDANT COLUMNS ────────────────────────────────────────────────
df = df.drop(columns=[
    'normalized_salary', 'min_salary', 'max_salary',
    'pay_period', 'remote_allowed', 'posted_timestamp'
])

# ── 10. FINAL QUALITY CHECK ──────────────────────────────────────────────────
print("\n=== CLEANED SHAPE ===")
print(df.shape)
print("\n=== CLEANED COLUMNS ===")
print(df.columns.tolist())
print("\n=== NULL COUNTS ===")
print(df.isnull().sum())
print("\n=== SAMPLE ===")
print(df.head(3))

# ── 11. SAVE CLEANED DATA ────────────────────────────────────────────────────
os.makedirs(r"C:\Users\Dinesh chandra reddy\TalentLens-AI\data\cleaned", exist_ok=True)
df.to_csv(r"C:\Users\Dinesh chandra reddy\TalentLens-AI\data\cleaned\jobs_cleaned.csv", index=False)
print("\n✅ Cleaned data saved successfully!")
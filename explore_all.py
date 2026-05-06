import pandas as pd

files = {
    "companies"         : r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\companies\companies.csv",
    "company_industries": r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\companies\company_industries.csv",
    "job_skills"        : r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\jobs\job_skills.csv",
    "salaries"          : r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\jobs\salaries.csv",
    "job_industries"    : r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\jobs\job_industries.csv",
    "skills"            : r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\mappings\skills.csv",
    "industries"        : r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\mappings\industries.csv",
}

for name, path in files.items():
    df = pd.read_csv(path)
    print(f"\n{'='*50}")
    print(f"📄 {name}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(df.head(2))
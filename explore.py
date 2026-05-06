import pandas as pd

# Load main postings file
df = pd.read_csv(r"C:\Users\Dinesh chandra reddy\linkedin-job-postings\postings.csv")

print("=== SHAPE ===")
print(df.shape)

print("\n=== COLUMNS ===")
print(df.columns.tolist())

print("\n=== SAMPLE (3 rows) ===")
print(df.head(3))

print("\n=== NULL COUNTS ===")
print(df.isnull().sum())
import zipfile
import os

zip_path = r"C:\Users\Dinesh chandra reddy\linkedin-job-postings.zip"
extract_path = r"C:\Users\Dinesh chandra reddy\linkedin-job-postings"

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_path)
    print("Extracted files:")
    for name in z.namelist():
        print(" -", name)
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import pandas as pd

app = Flask(__name__, static_folder='.', static_url_path='')
engine = create_engine("mysql+pymysql://root:Admin123@localhost/talentlens")

def q(sql):
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn).to_dict(orient='records')

@app.route('/')
def index():
    return app.send_static_file('dashboard.html')

@app.route('/api/kpis')
def kpis():
    with engine.connect() as conn:
        total    = conn.execute(text("SELECT COUNT(*) AS c FROM jobs")).fetchone()[0]
        companies= conn.execute(text("SELECT COUNT(DISTINCT company_id) FROM jobs")).fetchone()[0]
        remote   = conn.execute(text("SELECT ROUND(SUM(is_remote)*100.0/COUNT(*),1) FROM jobs")).fetchone()[0]
        salary   = conn.execute(text("SELECT ROUND(AVG(med_salary),0) FROM salaries WHERE med_salary IS NOT NULL")).fetchone()[0]
    return jsonify(total_jobs=int(total), companies=int(companies),
                   remote_pct=float(remote), avg_salary=float(salary))

@app.route('/api/skills')
def skills():
    return jsonify(q("""
        SELECT s.skill_name, COUNT(js.job_id) AS demand
        FROM job_skills js JOIN skills s ON js.skill_abr = s.skill_abr
        GROUP BY s.skill_name ORDER BY demand DESC LIMIT 12
    """))

@app.route('/api/remote')
def remote():
    return jsonify(q("""
        SELECT CASE WHEN is_remote=1 THEN 'Remote' ELSE 'Onsite' END AS work_mode,
               COUNT(*) AS total FROM jobs GROUP BY is_remote
    """))

@app.route('/api/cities')
def cities():
    return jsonify(q("""
        SELECT city, COUNT(*) AS job_count FROM jobs
        WHERE city IS NOT NULL AND city != '' AND city != 'United States'
        GROUP BY city ORDER BY job_count DESC LIMIT 10
    """))

@app.route('/api/salary_exp')
def salary_exp():
    return jsonify(q("""
        SELECT j.experience_level, ROUND(AVG(s.med_salary),0) AS avg_salary
        FROM jobs j JOIN salaries s ON j.job_id = s.job_id
        WHERE s.med_salary IS NOT NULL AND j.experience_level != 'Not Specified'
        GROUP BY j.experience_level ORDER BY avg_salary DESC
    """))

@app.route('/api/industries')
def industries():
    return jsonify(q("""
        SELECT i.industry_name, COUNT(ji.job_id) AS job_count
        FROM job_industries ji JOIN industries i ON ji.industry_id = i.industry_id
        GROUP BY i.industry_name ORDER BY job_count DESC LIMIT 10
    """))

@app.route('/api/top_jobs')
def top_jobs():
    return jsonify(q("""
        SELECT j.title, ROUND(AVG(s.med_salary),0) AS avg_salary, COUNT(*) AS job_count
        FROM jobs j JOIN salaries s ON j.job_id = s.job_id
        WHERE s.med_salary IS NOT NULL AND s.med_salary < 500000
        GROUP BY j.title HAVING job_count >= 5
        ORDER BY avg_salary DESC LIMIT 8
    """))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
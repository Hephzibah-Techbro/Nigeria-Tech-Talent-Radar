
import pandas as pd

from src.cleaning.clean_jobs import clean_jobs
from src.skills.extract_skills import (
    classify_technology_jobs,
    extract_skills
)


def test_clean_jobs_removes_duplicate_urls():

    data = pd.DataFrame({
        "title": ["Data Analyst", "Data Analyst"],
        "job_url": ["job1", "job1"],
        "hiring_firm": ["Company A", "Company A"]
    })

    cleaned = clean_jobs(data)

    assert len(cleaned) == 1


def test_classify_technology_jobs():

    data = pd.DataFrame({
        "title": ["Python Developer", "Sales Officer"],
        "job_function": ["", ""],
        "details": ["Experience with Python", "Sales experience"],
        "info": ["", ""]
    })

    tech_jobs = classify_technology_jobs(data)

    assert len(tech_jobs) == 1
    assert tech_jobs.iloc[0]["title"] == "Python Developer"


def test_extract_skills():

    data = pd.DataFrame({
        "title": ["Python Developer", "Data Analyst"],
        "details": [
            "Python and SQL experience",
            "Excel and Power BI experience"
        ],
        "info": ["", ""]
    })

    skills = extract_skills(data)

    skill_names = skills["skill"].tolist()

    assert "Python" in skill_names
    assert "SQL" in skill_names
    assert "Excel" in skill_names
    assert "Power BI" in skill_names

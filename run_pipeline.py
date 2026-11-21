
from pathlib import Path
from datetime import datetime

from src.ingestion.load_jobs import load_jobs
from src.cleaning.clean_jobs import clean_jobs
from src.skills.extract_skills import (
    classify_technology_jobs,
    extract_skills
)


def main():

    # Project directories
    project_root = Path(__file__).resolve().parent

    raw_file = (
        project_root
        / "data"
        / "raw"
        / "jobs"
        / "combined_jobs.csv"
    )

    output_dir = project_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\nNIGERIA TECH TALENT RADAR")
    print("=========================")

    # 1. Extract
    print("\n1. Loading raw job listings...")
    raw_jobs = load_jobs(raw_file)

    # 2. Transform and clean
    print("\n2. Cleaning job listings...")
    cleaned_jobs = clean_jobs(raw_jobs)

    # 3. Classify technology jobs
    print("\n3. Identifying technology jobs...")
    tech_jobs = classify_technology_jobs(cleaned_jobs)

    # 4. Extract skills
    print("\n4. Extracting technology skills...")
    skills = extract_skills(tech_jobs)

    # 5. Save datasets
    print("\n5. Saving processed datasets...")

    cleaned_jobs.to_csv(
        output_dir / "jobs_cleaned.csv",
        index=False
    )

    tech_jobs.to_csv(
        output_dir / "tech_jobs.csv",
        index=False
    )

    skills.to_csv(
        output_dir / "tech_skills.csv",
        index=False
    )

    # 6. Generate report
    duplicate_count = len(raw_jobs) - len(cleaned_jobs)

    top_skills = (
        skills.head(15).to_string(index=False)
        if not skills.empty
        else "No skills identified."
    )

    location_summary = (
        tech_jobs["location"]
        .value_counts()
        .head(10)
        .to_string()
    )

    function_summary = (
        tech_jobs["job_function"]
        .value_counts()
        .head(10)
        .to_string()
    )

    report = f"""
NIGERIA TECH TALENT RADAR
DATA PROCESSING REPORT
================================

Processing date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

DATASET SUMMARY
---------------
Original job listings: {len(raw_jobs)}
Cleaned job listings: {len(cleaned_jobs)}
Duplicate records removed: {duplicate_count}
Technology-related listings identified: {len(tech_jobs)}

TECHNOLOGY JOB CLASSIFICATION
-----------------------------
Technology listings were identified using keyword matching
against job titles, job functions and job descriptions.

TOP TECHNOLOGY SKILLS
---------------------
{top_skills}

TOP TECHNOLOGY JOB LOCATIONS
----------------------------
{location_summary}

JOB FUNCTION DISTRIBUTION
-------------------------
{function_summary}

OUTPUT FILES
------------
jobs_cleaned.csv
tech_jobs.csv
tech_skills.csv
processing_report.txt

DATA LIMITATIONS
----------------
The source dataset's original collection date is unknown.

Technology job classification uses keyword matching and
may include false positives or miss relevant listings.

Skill counts represent job listings mentioning each skill.
They do not represent verified employer requirements.

Relative posting dates are preserved as originally supplied.
No calendar dates have been inferred.

This pipeline processes a historical CSV dataset.
It does not automatically collect live job listings.
"""

    report_file = output_dir / "processing_report.txt"

    report_file.write_text(report, encoding="utf-8")

    # 7. Display summary
    print("\nPIPELINE COMPLETED SUCCESSFULLY")
    print("================================")
    print(f"Raw jobs: {len(raw_jobs)}")
    print(f"Cleaned jobs: {len(cleaned_jobs)}")
    print(f"Duplicates removed: {duplicate_count}")
    print(f"Technology jobs: {len(tech_jobs)}")
    print(f"Skills identified: {len(skills)}")

    print("\nTop 10 skills:")
    print(skills.head(10).to_string(index=False))

    print(f"\nProcessed files saved in: {output_dir}")


if __name__ == "__main__":
    main()

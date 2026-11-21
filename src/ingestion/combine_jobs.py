
import pandas as pd
from pathlib import Path


def combine_job_sources():

    project_root = Path(__file__).resolve().parents[2]

    # Load original Nigerian job dataset
    original_file = (
        project_root / "data" / "raw" / "jobs" / "nigeria_jobs_raw.csv"
    )

    original_jobs = pd.read_csv(original_file)

    # Load Moniepoint API dataset
    moniepoint_file = (
        project_root / "data" / "raw" / "jobs" / "moniepoint_jobs.csv"
    )

    moniepoint_jobs = pd.read_csv(moniepoint_file)

    # Standardise column names
    original_jobs.columns = (
        original_jobs.columns.str.strip().str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )

    # Add missing columns to Moniepoint data
    moniepoint_jobs["name"] = "Moniepoint"
    moniepoint_jobs["hiring_firm"] = "Moniepoint"
    moniepoint_jobs["job_function"] = ""
    moniepoint_jobs["hiring_firm_url"] = ""
    moniepoint_jobs["industry"] = "Financial Technology"
    moniepoint_jobs["salary"] = ""
    moniepoint_jobs["info"] = ""

    # Keep common columns
    common_columns = [
        "name",
        "job_url",
        "hiring_firm",
        "hiring_firm_url",
        "job_function",
        "title",
        "date_posted",
        "location",
        "job_type",
        "industry",
        "salary",
        "details",
        "info"
    ]

    original_jobs = original_jobs.reindex(columns=common_columns)
    moniepoint_jobs = moniepoint_jobs.reindex(columns=common_columns)

    # Combine both datasets
    combined_jobs = pd.concat(
        [original_jobs, moniepoint_jobs],
        ignore_index=True
    )

    # Save combined dataset
    output_file = (
        project_root / "data" / "raw" / "jobs" / "combined_jobs.csv"
    )

    combined_jobs.to_csv(output_file, index=False)

    print("JOB DATA SOURCES COMBINED SUCCESSFULLY")
    print("--------------------------------------")
    print("Original dataset:", len(original_jobs))
    print("Moniepoint dataset:", len(moniepoint_jobs))
    print("Combined dataset:", len(combined_jobs))
    print("Saved to:", output_file)

    return combined_jobs


if __name__ == "__main__":
    combine_job_sources()

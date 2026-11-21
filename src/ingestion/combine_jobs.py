
import pandas as pd
from pathlib import Path


def combine_job_sources():

    project_root = Path(__file__).resolve().parents[2]

    jobs_folder = project_root / "data" / "raw" / "jobs"

    # 1. Load original Nigerian job dataset
    original_jobs = pd.read_csv(
        jobs_folder / "nigeria_jobs_raw.csv"
    )

    # 2. Load Moniepoint jobs
    moniepoint_jobs = pd.read_csv(
        jobs_folder / "moniepoint_jobs.csv"
    )

    # 3. Load OPay jobs
    opay_jobs = pd.read_csv(
        jobs_folder / "opay_jobs.csv"
    )

    # Standardise original dataset column names
    original_jobs.columns = (
        original_jobs.columns.str.strip().str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )

    # Prepare Moniepoint data
    moniepoint_jobs["name"] = "Moniepoint"
    moniepoint_jobs["hiring_firm"] = "Moniepoint"
    moniepoint_jobs["job_function"] = ""
    moniepoint_jobs["hiring_firm_url"] = ""
    moniepoint_jobs["industry"] = "Financial Technology"
    moniepoint_jobs["salary"] = ""
    moniepoint_jobs["info"] = ""

    # Prepare OPay data
    opay_jobs["name"] = "OPay"
    opay_jobs["hiring_firm"] = "OPay"
    opay_jobs["hiring_firm_url"] = "https://careers.opayweb.com/"
    opay_jobs["job_function"] = opay_jobs["department"]
    opay_jobs["job_url"] = ""
    opay_jobs["job_type"] = opay_jobs["employment_type"]
    opay_jobs["industry"] = "Financial Technology"
    opay_jobs["salary"] = ""

    opay_jobs["details"] = (
        "Department: " + opay_jobs["department"].fillna("").astype(str)
        + "; Work mode: " + opay_jobs["work_mode"].fillna("").astype(str)
        + "; States: " + opay_jobs["states"].fillna("").astype(str)
        + "; Localities: " + opay_jobs["localities"].fillna("").astype(str)
    )

    opay_jobs["info"] = (
        "Application deadline: "
        + opay_jobs["application_deadline"].fillna("Not specified").astype(str)
        + "; Status: "
        + opay_jobs["status"].fillna("").astype(str)
    )

    # Standard columns for all sources
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

    # Keep only common columns
    original_jobs = original_jobs.reindex(columns=common_columns)
    moniepoint_jobs = moniepoint_jobs.reindex(columns=common_columns)
    opay_jobs = opay_jobs.reindex(columns=common_columns)

    # Combine all three sources
    combined_jobs = pd.concat(
        [original_jobs, moniepoint_jobs, opay_jobs],
        ignore_index=True
    )

    # Save combined dataset
    output_file = jobs_folder / "combined_jobs.csv"

    combined_jobs.to_csv(output_file, index=False)

    print("JOB DATA SOURCES COMBINED SUCCESSFULLY")
    print("--------------------------------------")
    print("Jobberman dataset:", len(original_jobs))
    print("Moniepoint dataset:", len(moniepoint_jobs))
    print("OPay dataset:", len(opay_jobs))
    print("Combined dataset:", len(combined_jobs))
    print("Saved to:", output_file)

    return combined_jobs


if __name__ == "__main__":
    combine_job_sources()

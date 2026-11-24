import pandas as pd
from pathlib import Path

from src.common.database import get_db_connection


def load_jobs_to_database():
    """Load cleaned job listings into PostgreSQL."""

    project_root = Path(__file__).resolve().parents[2]

    csv_file = (
        project_root
        / "data"
        / "processed"
        / "jobs_cleaned.csv"
    )

    jobs = pd.read_csv(csv_file)

    # Exclude records without valid job URLs
    valid_urls = (
        jobs["job_url"].notna()
        & jobs["job_url"].astype(str).str.strip().ne("")
    )

    skipped_jobs = len(jobs) - valid_urls.sum()
    jobs = jobs[valid_urls].copy()

    print(f"Jobs ready for loading: {len(jobs)}")
    print(f"Jobs skipped (missing URLs): {skipped_jobs}")

    insert_query = """
        INSERT INTO job_listings (
            title,
            job_url,
            hiring_firm,
            hiring_firm_url,
            job_function,
            location,
            job_type,
            industry,
            salary,
            details,
            info,
            date_posted_raw,
            date_posted_days_ago,
            estimated_posting_date,
            date_estimated,
            collection_date
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        ON CONFLICT (job_url) DO NOTHING;
    """

    records = []

    for _, row in jobs.iterrows():

        days_ago = (
            None
            if pd.isna(row["date_posted_days_ago"])
            else int(row["date_posted_days_ago"])
        )

        estimated_date = (
            None
            if pd.isna(row["estimated_posting_date"])
            else pd.to_datetime(row["estimated_posting_date"]).date()
        )

        collection_date = pd.to_datetime(
            row["collection_date"]
        ).date()

        date_estimated = bool(row["date_estimated"])

        records.append((
            row["title"],
            row["job_url"],
            None if pd.isna(row["hiring_firm"]) else row["hiring_firm"],
            None if pd.isna(row["hiring_firm_url"]
                            ) else row["hiring_firm_url"],
            None if pd.isna(row["job_function"]) else row["job_function"],
            None if pd.isna(row["location"]) else row["location"],
            None if pd.isna(row["job_type"]) else row["job_type"],
            None if pd.isna(row["industry"]) else row["industry"],
            None if pd.isna(row["salary"]) else row["salary"],
            None if pd.isna(row["details"]) else row["details"],
            None if pd.isna(row["info"]) else row["info"],
            None if pd.isna(row["date_posted_raw"]
                            ) else row["date_posted_raw"],
            days_ago,
            estimated_date,
            date_estimated,
            collection_date
        ))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.executemany(insert_query, records)
        connection.commit()

        print(f"Job records processed: {len(records)}")

        cursor.execute("SELECT COUNT(*) FROM job_listings")
        total_jobs = cursor.fetchone()[0]

        print(f"Total jobs in PostgreSQL: {total_jobs}")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_jobs_to_database()

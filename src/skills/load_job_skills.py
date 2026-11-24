import pandas as pd
from pathlib import Path
from psycopg2.extras import execute_values

from src.common.database import get_db_connection


def load_job_skills():
    """Load individual job-skill relationships into PostgreSQL."""

    project_root = Path(__file__).resolve().parents[2]

    csv_file = (
        project_root
        / "data"
        / "processed"
        / "job_skills.csv"
    )

    job_skills = pd.read_csv(csv_file)

    # Remove records with missing job URLs or skill names
    job_skills = job_skills.dropna(
        subset=["job_url", "skill"]
    )

    # Remove extra spaces
    job_skills["job_url"] = job_skills["job_url"].str.strip()
    job_skills["skill"] = job_skills["skill"].str.strip()

    job_skills = job_skills[
        (job_skills["job_url"] != "")
        & (job_skills["skill"] != "")
    ].drop_duplicates()

    # Prepare unique skill names
    skill_names = job_skills["skill"].unique().tolist()

    # Prepare job-skill records
    records = list(
        job_skills[["job_url", "skill"]].itertuples(
            index=False,
            name=None
        )
    )

    print(f"Job-skill records ready: {len(records)}")
    print(f"Unique skills identified: {len(skill_names)}")

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Add any missing skills to the skills dimension
        execute_values(
            cursor,
            """
            INSERT INTO skills (skill_name)
            VALUES %s
            ON CONFLICT (skill_name) DO NOTHING;
            """,
            [(skill,) for skill in skill_names]
        )

        # Link each job to its corresponding skill
        insert_query = """
            INSERT INTO job_skills (job_id, skill_id)
            SELECT
                jobs.job_id,
                skills.skill_id
            FROM (VALUES %s) AS source(job_url, skill_name)
            JOIN job_listings AS jobs
                ON jobs.job_url = source.job_url
            JOIN skills
                ON skills.skill_name = source.skill_name
            ON CONFLICT (job_id, skill_id) DO NOTHING;
        """

        execute_values(
            cursor,
            insert_query,
            records,
            page_size=1000
        )

        connection.commit()

        # Verify total relationships
        cursor.execute(
            "SELECT COUNT(*) FROM job_skills"
        )

        total_relationships = cursor.fetchone()[0]

        print(
            f"Total job-skill relationships in PostgreSQL: "
            f"{total_relationships}"
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_job_skills()

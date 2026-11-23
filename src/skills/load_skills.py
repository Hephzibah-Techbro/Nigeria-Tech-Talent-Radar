import pandas as pd
from pathlib import Path

from src.common.database import get_db_connection


# Locate the project's root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Define the input file paths
JOB_SKILLS_FILE = BASE_DIR / "data/processed/tech_skills.csv"
SKILL_MAPPING_FILE = BASE_DIR / "data/reference/skill_mapping.csv"
CURRICULUM_FILE = BASE_DIR / "data/raw/training/training_curriculum.csv"


def load_skill_data():
    # Read the job-market skills
    job_skills = pd.read_csv(JOB_SKILLS_FILE)

    # Read the approved skill mappings
    skill_mapping = pd.read_csv(SKILL_MAPPING_FILE)

    # Read the training curriculum
    curriculum = pd.read_csv(CURRICULUM_FILE)

    print(f"Job-market skills loaded: {len(job_skills)}")
    print(f"Skill mappings loaded: {len(skill_mapping)}")
    print(f"Curriculum records loaded: {len(curriculum)}")

    return job_skills, skill_mapping, curriculum


def prepare_skill_data(job_skills, skill_mapping, curriculum):
    # Create a lookup dictionary from the approved mapping file
    skill_lookup = {
        row["original_skill"].strip().lower(): row["standard_skill"].strip()
        for _, row in skill_mapping.iterrows()
    }

    # Collect the standardised skills from the job-market dataset
    all_skills = set(job_skills["skill"].str.strip())

    # Prepare the curriculum-to-skill relationships
    curriculum_skill_records = []

    for _, row in curriculum.iterrows():
        skills = row["skills_acquired"].split(";")

        for skill in skills:
            original_skill = skill.strip()
            lookup_key = original_skill.lower()

            if lookup_key not in skill_lookup:
                raise ValueError(
                    f"No approved mapping found for: {original_skill}")

            standard_skill = skill_lookup[lookup_key]

            all_skills.add(standard_skill)

            curriculum_skill_records.append(
                (row["curriculum_id"], standard_skill)
            )

    # Sort the skills to keep the insertion order consistent
    all_skills = sorted(all_skills)

    # Remove duplicate curriculum-skill relationships
    curriculum_skill_records = sorted(set(curriculum_skill_records))

    print(f"\nUnique standardised skills prepared: {len(all_skills)}")
    print(
        f"Curriculum-skill relationships prepared: {len(curriculum_skill_records)}")

    return all_skills, curriculum_skill_records


def insert_skills(all_skills, curriculum_skill_records):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        # Insert unique skills into PostgreSQL
        skill_query = """
            INSERT INTO skills (skill_name)
            VALUES (%s)
            ON CONFLICT (skill_name) DO NOTHING;
        """

        skill_records = [(skill,) for skill in all_skills]

        cursor.executemany(skill_query, skill_records)

        print(f"Skills processed: {len(all_skills)}")

        # Retrieve the skill IDs from PostgreSQL
        cursor.execute(
            """
            SELECT skill_id, skill_name
            FROM skills
            WHERE skill_name = ANY(%s);
            """,
            (all_skills,)
        )

        skill_ids = {
            skill_name: skill_id
            for skill_id, skill_name in cursor.fetchall()
        }

        # Prepare curriculum-skill relationships using skill IDs
        relationship_records = []

        for curriculum_id, skill_name in curriculum_skill_records:
            skill_id = skill_ids[skill_name]

            relationship_records.append(
                (curriculum_id, skill_id)
            )

        # Insert curriculum-skill relationships
        relationship_query = """
            INSERT INTO curriculum_skills (
                curriculum_id,
                skill_id
            )
            VALUES (%s, %s)
            ON CONFLICT (curriculum_id, skill_id) DO NOTHING;
        """

        cursor.executemany(
            relationship_query,
            relationship_records
        )

        print(
            f"Curriculum-skill relationships processed: "
            f"{len(relationship_records)}"
        )

        # Save both sets of changes together
        connection.commit()

        print("Skills and curriculum relationships successfully saved!")

    except Exception:
        connection.rollback()
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()

        connection.close()


if __name__ == "__main__":
    # Read the input datasets
    job_skills, skill_mapping, curriculum = load_skill_data()

    # Prepare the standardised skills and curriculum relationships
    all_skills, curriculum_skill_records = prepare_skill_data(
        job_skills,
        skill_mapping,
        curriculum
    )

    # Insert skills and curriculum relationships into PostgreSQL
    insert_skills(all_skills, curriculum_skill_records)

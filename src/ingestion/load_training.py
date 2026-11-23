import pandas as pd
from pathlib import Path

from src.common.database import get_db_connection


BASE_DIR = Path(__file__).resolve().parents[2]

PROGRAMMES_FILE = BASE_DIR / "data/raw/training/training_programmes.csv"
CURRICULUM_FILE = BASE_DIR / "data/raw/training/training_curriculum.csv"


def load_training_data():
    programmes = pd.read_csv(PROGRAMMES_FILE)
    curriculum = pd.read_csv(CURRICULUM_FILE)

    print(f"Training programmes loaded: {len(programmes)}")
    print(f"Curriculum records loaded: {len(curriculum)}")

    return programmes, curriculum


def insert_training_data(programmes, curriculum):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        print("Connected to PostgreSQL successfully!")

        # Insert training programmes into PostgreSQL
        programme_query = """
            INSERT INTO training_programmes (
                programme_id,
                programme_name,
                provider,
                duration,
                format,
                country,
                target_audience,
                programme_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (programme_id) DO UPDATE SET
                programme_name = EXCLUDED.programme_name,
                provider = EXCLUDED.provider,
                duration = EXCLUDED.duration,
                format = EXCLUDED.format,
                country = EXCLUDED.country,
                target_audience = EXCLUDED.target_audience,
                programme_url = EXCLUDED.programme_url;
        """

        programme_records = programmes[
            [
                "programme_id",
                "programme_name",
                "provider",
                "duration",
                "format",
                "country",
                "target_audience",
                "programme_url"
            ]
        ]

        cursor.executemany(
            programme_query,
            list(programme_records.itertuples(index=False, name=None))
        )

        print(f"Training programmes inserted: {len(programmes)}")

        # Insert curriculum records into PostgreSQL
        curriculum_query = """
            INSERT INTO training_curricula (
                curriculum_id,
                programme_id,
                technology_track,
                module_name,
                topics,
                skills_acquired,
                source_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (curriculum_id) DO UPDATE SET
                programme_id = EXCLUDED.programme_id,
                technology_track = EXCLUDED.technology_track,
                module_name = EXCLUDED.module_name,
                topics = EXCLUDED.topics,
                skills_acquired = EXCLUDED.skills_acquired,
                source_url = EXCLUDED.source_url;
        """

        curriculum_records = curriculum[
            [
                "curriculum_id",
                "programme_id",
                "technology_track",
                "module_name",
                "topics",
                "skills_acquired",
                "source_url"
            ]
        ]

        cursor.executemany(
            curriculum_query,
            list(curriculum_records.itertuples(index=False, name=None))
        )

        print(f"Curriculum records inserted: {len(curriculum)}")

        # Save all changes to PostgreSQL
        connection.commit()

        print("Training data successfully saved to PostgreSQL!")

    except Exception:
        connection.rollback()
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    programmes, curriculum = load_training_data()

    print("\nTraining programmes:")
    print(programmes[["programme_id", "programme_name"]])

    print("\nCurriculum records:")
    print(curriculum[["curriculum_id", "module_name"]])

    insert_training_data(programmes, curriculum)

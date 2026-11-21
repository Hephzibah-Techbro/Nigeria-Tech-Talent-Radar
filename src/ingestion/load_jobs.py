
import pandas as pd
from pathlib import Path


def load_jobs(file_path):
    """
    Load Nigerian job listings from a CSV file.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print(f"Successfully loaded {len(df)} job listings.")

    return df


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    file_path = (
        project_root
        / "data"
        / "raw"
        / "jobs"
        / "nigeria_jobs_raw.csv"
    )

    jobs = load_jobs(file_path)

    print("\nDataset columns:")
    print(jobs.columns.tolist())

    print("\nFirst five records:")
    print(jobs.head())

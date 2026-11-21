import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

PROGRAMMES_FILE = BASE_DIR / "data/raw/training/training_programmes.csv"
CURRICULUM_FILE = BASE_DIR / "data/raw/training/training_curriculum.csv"


def load_training_data():
    programmes = pd.read_csv(PROGRAMMES_FILE)
    curriculum = pd.read_csv(CURRICULUM_FILE)

    print(f"Training programmes loaded: {len(programmes)}")
    print(f"Curriculum records loaded: {len(curriculum)}")

    return programmes, curriculum


if __name__ == "__main__":
    programmes, curriculum = load_training_data()

    print("\nTraining programmes:")
    print(programmes[["programme_id", "programme_name"]])

    print("\nCurriculum records:")
    print(curriculum[["curriculum_id", "module_name"]])
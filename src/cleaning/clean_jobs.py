

import pandas as pd
import re


def clean_jobs(df):
    """
    Clean Nigerian job listings while preserving original date information.
    """

    df = df.copy()

    # 1. Standardise column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )

    # 2. Remove extra spaces from text fields
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    # 3. Replace empty strings with missing values
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # 4. Remove duplicate job URLs only
    if "job_url" in df.columns:
        df = df.drop_duplicates(
            subset=["job_url"],
            keep="first"
        )

    # 5. Handle missing values in important columns
    important_columns = [
        "title",
        "hiring_firm",
        "location",
        "job_function",
        "industry",
        "salary",
        "job_type"
    ]

    for column in important_columns:
        if column in df.columns:
            df[column] = df[column].fillna("Not specified")

    # 6. Preserve original relative dates
    if "date_posted" in df.columns:

        df["date_posted_raw"] = df["date_posted"]

        def convert_relative_date(value):
            if pd.isna(value):
                return pd.NA

            value = str(value).strip().lower()

            if value == "today":
                return 0

            if value == "yesterday":
                return 1

            match = re.match(r"(\d+)\s+(day|week|month)s?\s+ago", value)

            if match:
                number = int(match.group(1))
                unit = match.group(2)

                if unit == "day":
                    return number
                elif unit == "week":
                    return number * 7
                elif unit == "month":
                    return number * 30

            return pd.NA

        df["date_posted_days_ago"] = (
            df["date_posted_raw"].apply(convert_relative_date)
        )

    return df


if __name__ == "__main__":
    print("Cleaning module is ready.")

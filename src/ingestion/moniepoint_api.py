
import requests
import pandas as pd


def fetch_moniepoint_jobs():

    url = "https://boards-api.greenhouse.io/v1/boards/moniepoint/jobs?content=true"
    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()

    jobs = data.get("jobs", [])

    records = []

    for job in jobs:
        records.append({
            "title": job.get("title"),
            "location": job.get("location", {}).get("name"),
            "job_url": job.get("absolute_url"),
            "date_posted": job.get("updated_at"),
            "hiring_firm": "Moniepoint",
            "details": job.get("content")
        })

    return pd.DataFrame(records)


if __name__ == "__main__":

    jobs = fetch_moniepoint_jobs()

    print(f"Moniepoint jobs retrieved: {len(jobs)}")

    print(jobs[["title", "location", "job_url"]].head(10))

    jobs.to_csv(
        "data/raw/jobs/moniepoint_jobs.csv",
        index=False
    )

    print("Moniepoint jobs saved successfully.")

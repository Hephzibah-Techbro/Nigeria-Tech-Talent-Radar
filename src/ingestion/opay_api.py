
import requests
import pandas as pd
import os

API_URL = "https://careers.opayweb.com/api/job-listings"

def fetch_opay_jobs():
    params = {
        "page": 0,
        "size": 100
    }

    response = requests.get(API_URL, params=params, timeout=60)
    response.raise_for_status()

    result = response.json()
    jobs = result.get("data", [])

    records = []

    for job in jobs:
        location_info = job.get("jobLocation") or {}
        states = location_info.get("states", [])

        state_names = "; ".join(
            state.get("stateName", "")
            for state in states
            if state.get("stateName")
        )

        localities = "; ".join(
            f"{state.get('stateName', '')}: {', '.join(state.get('localities', []))}"
            for state in states
            if state.get("localities")
        )

        records.append({
            "source": "OPay Careers",
            "job_id": job.get("id"),
            "title": job.get("title"),
            "location": "Nationwide" if location_info.get("nationwideRecruitment") else state_names,
            "states": state_names,
            "localities": localities,
            "department": (job.get("department") or {}).get("name"),
            "work_mode": job.get("workMode"),
            "employment_type": job.get("employmentType"),
            "status": job.get("status"),
            "date_posted": job.get("createdAt"),
            "application_deadline": job.get("applicationDeadline")
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = fetch_opay_jobs()

    output_folder = "data/raw/jobs"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "opay_jobs.csv")
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"Successfully collected {len(df)} OPay vacancies.")
    print(f"Saved to: {output_file}")
    print(df[["title", "location", "department"]].to_string(index=False))


import pandas as pd
import re


# Technology-related job keywords
TECH_KEYWORDS = [
    "data analyst",
    "data scientist",
    "data engineer",
    "business intelligence",
    "machine learning",
    "artificial intelligence",
    "software developer",
    "software engineer",
    "web developer",
    "frontend developer",
    "front end developer",
    "backend developer",
    "back end developer",
    "full stack developer",
    "mobile developer",
    "python developer",
    "cybersecurity",
    "cyber security",
    "cloud engineer",
    "cloud architect",
    "devops",
    "network engineer",
    "database administrator",
    "database engineer",
    "systems administrator",
    "information technology",
    "it support",
    "ui/ux",
    "ux designer",
    "ui designer",
    "product designer",
    "product manager",
    "product owner",
    "technical project manager",
    "digital marketing",
    "seo specialist",
    "technical support",
    "computer vision",
    "nlp engineer",
    "qa engineer",
    "quality assurance engineer"
]


# Skills dictionary
SKILLS = {
    "Python": ["python"],
    "SQL": ["sql"],
    "Excel": ["excel"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "TypeScript": ["typescript"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "PHP": ["php"],
    "C++": ["c++"],
    "C#": ["c#"],
    "AWS": ["aws", "amazon web services"],
    "Microsoft Azure": ["azure"],
    "Google Cloud": ["google cloud", "gcp"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes"],
    "Machine Learning": ["machine learning"],
    "Artificial Intelligence": ["artificial intelligence"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Science": ["data science"],
    "Data Engineering": ["data engineering"],
    "Cybersecurity": ["cybersecurity", "cyber security"],
    "Networking": ["networking"],
    "UI/UX Design": ["ui/ux", "user experience", "user interface"],
    "Figma": ["figma"],
    "Project Management": ["project management"],
    "Agile": ["agile"],
    "Scrum": ["scrum"],
    "SEO": ["seo", "search engine optimization"],
    "Digital Marketing": ["digital marketing"],
    "Git": ["git", "github"]
}


def classify_technology_jobs(df):
    """
    Identify technology-related job listings.
    """

    df = df.copy()

    search_columns = [
        col for col in [
            "title",
            "job_function",
            "details",
            "info"
        ] if col in df.columns
    ]

    search_text = (
        df[search_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    # Strong technology job functions
    strong_functions = [
        "software & data",
        "engineering & technology"
    ]

    function_match = (
        df["job_function"]
        .fillna("")
        .str.lower()
        .apply(
            lambda value: any(
                category in value
                for category in strong_functions
            )
        )
    )

    keyword_pattern = "|".join(
        re.escape(keyword) for keyword in TECH_KEYWORDS
    )

    keyword_match = search_text.str.contains(
        keyword_pattern,
        case=False,
        regex=True,
        na=False
    )

    tech_jobs = df[function_match | keyword_match].copy()

    return tech_jobs


def extract_skills(tech_jobs):
    """
    Extract technology skills from job descriptions and titles.
    """

    records = []

    search_columns = [
        col for col in ["title", "details", "info"]
        if col in tech_jobs.columns
    ]

    search_text = (
        tech_jobs[search_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    for skill, keywords in SKILLS.items():

        pattern = "|".join(
            r"(?<!\w)" + re.escape(word) + r"(?!\w)"
            for word in keywords
        )

        matches = search_text.str.contains(
            pattern,
            case=False,
            regex=True,
            na=False
        )

        count = int(matches.sum())

        if count > 0:
            records.append({
                "skill": skill,
                "job_count": count
            })

    skills_df = pd.DataFrame(records)

    if not skills_df.empty:
        skills_df = skills_df.sort_values(
            by="job_count",
            ascending=False
        ).reset_index(drop=True)

    return skills_df

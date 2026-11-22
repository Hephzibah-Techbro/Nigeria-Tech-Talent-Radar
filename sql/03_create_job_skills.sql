-- Create the job_skills table if it does not already exist
CREATE TABLE IF NOT EXISTS job_skills (

    -- References the job listing that requires the skill
    job_id BIGINT NOT NULL REFERENCES job_listings(job_id),

    -- References the skill required by the job
    skill_id BIGINT NOT NULL REFERENCES skills(skill_id),

    -- Prevents the same skill from being linked to a job more than once
    PRIMARY KEY (job_id, skill_id)
    );

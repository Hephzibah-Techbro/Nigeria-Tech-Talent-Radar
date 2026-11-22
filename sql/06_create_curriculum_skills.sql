-- Create the curriculum_skills table if it does not already exist
CREATE TABLE IF NOT EXISTS curriculum_skills (

    -- References the curriculum record where the skill is taught
    curriculum_id TEXT NOT NULL REFERENCES training_curricula(curriculum_id),

    -- References the skill in the shared skills table
    skill_id BIGINT NOT NULL REFERENCES skills(skill_id),

    -- Prevents the same skill from being linked to a curriculum more than once
    PRIMARY KEY (curriculum_id, skill_id)
);
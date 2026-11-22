-- Create the skills table if it does not already exist
CREATE TABLE IF NOT EXISTS skills (

    -- Unique identifier for each skill
    skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- Name of the technology skill
    skill_name TEXT NOT NULL UNIQUE,

    -- Record creation timestamp
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
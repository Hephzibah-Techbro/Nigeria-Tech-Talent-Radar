
-- Create the training_curricula table if it does not already exist
CREATE TABLE IF NOT EXISTS training_curricula (

    -- Unique identifier for each curriculum record
    curriculum_id TEXT PRIMARY KEY,

    -- Links the curriculum record to a training programme
    programme_id TEXT NOT NULL REFERENCES training_programmes(programme_id),

    -- Curriculum details
    technology_track TEXT,
    module_name TEXT,
    topics TEXT,
    skills_acquired TEXT,
    source_url TEXT,

    -- Record creation timestamp
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
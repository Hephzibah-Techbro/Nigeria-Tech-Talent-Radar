-- Create the training_programmes table if it does not already exist
CREATE TABLE IF NOT EXISTS training_programmes (

    -- Unique identifier for each training programme
    programme_id TEXT PRIMARY KEY,

    -- General programme information
    programme_name TEXT NOT NULL,
    provider TEXT NOT NULL,
    duration TEXT,
    format TEXT,
    country TEXT,
    target_audience TEXT,
    programme_url TEXT,

    -- Record creation timestamp
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
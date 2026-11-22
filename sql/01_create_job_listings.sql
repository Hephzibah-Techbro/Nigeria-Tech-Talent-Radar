-- Create the job_listings table if it does not already exist
CREATE TABLE IF NOT EXISTS job_listings (

    -- Unique identifier for each job listing
    job_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- Basic job information
    title TEXT NOT NULL,
    job_url TEXT NOT NULL UNIQUE,
    hiring_firm TEXT,
    hiring_firm_url TEXT,

    -- Job details
    job_function TEXT,
    location TEXT,
    job_type TEXT,
    industry TEXT,
    salary TEXT,
    details TEXT,
    info TEXT,

    -- Job posting date information
    date_posted_raw TEXT,
    date_posted_days_ago INTEGER,
    estimated_posting_date DATE,
    date_estimated BOOLEAN,
    collection_date DATE NOT NULL,

    -- Warehouse record timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
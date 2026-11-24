SELECT *
FROM {{ source('raw', 'job_listings') }}
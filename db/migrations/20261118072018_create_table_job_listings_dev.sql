-- migrate:up
CREATE TABLE job_listings_dev (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source text NOT NULL,
    source_guid text NOT NULL,
    title text NOT NULL,
    company_name text NOT NULL,
    raw_data jsonb NOT NULL,
    fetched_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source, source_guid)
);

-- migrate:down
DROP TABLE job_listings_dev;
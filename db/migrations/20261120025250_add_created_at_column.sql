-- migrate:up
ALTER TABLE job_listings_dev
ADD COLUMN created_at timestamptz NOT NULL DEFAULT now();

ALTER TABLE job_listings
ADD COLUMN created_at timestamptz NOT NULL DEFAULT now();

-- migrate:down
ALTER TABLE job_listings_dev
DROP COLUMN created_at;

ALTER TABLE job_listings
DROP COLUMN created_at;
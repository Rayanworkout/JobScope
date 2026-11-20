-- migrate:up
ALTER TABLE job_listings_dev
RENAME COLUMN fetched_at TO last_fetched_at;

ALTER TABLE job_listings
RENAME COLUMN fetched_at TO last_fetched_at;

-- migrate:down
ALTER TABLE job_listings_dev
RENAME COLUMN last_fetched_at TO fetched_at

ALTER TABLE job_listings
RENAME COLUMN last_fetched_at TO fetched_at
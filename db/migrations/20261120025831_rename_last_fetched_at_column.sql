-- migrate:up
ALTER TABLE job_listings_dev
RENAME COLUMN last_fetched_at TO updated_at;

ALTER TABLE job_listings
RENAME COLUMN last_fetched_at TO updated_at;

-- migrate:down
ALTER TABLE job_listings_dev
RENAME COLUMN updated_at TO last_fetched_at

ALTER TABLE job_listings
RENAME COLUMN updated_at TO last_fetched_at
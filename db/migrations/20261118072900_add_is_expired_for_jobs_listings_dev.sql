-- migrate:up
ALTER TABLE job_listings_dev
ADD is_expired boolean;

-- migrate:down
ALTER TABLE job_listings_dev
DROP COLUMN IF EXISTS is_expired;
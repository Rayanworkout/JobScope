-- migrate:up
ALTER TABLE job_listings
ADD is_expired boolean;

-- migrate:down
ALTER TABLE job_listings
DROP COLUMN IF EXISTS is_expired;
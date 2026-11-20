-- migrate:up
ALTER TABLE job_listings_dev
ADD COLUMN description TEXT;

ALTER TABLE job_listings
ADD COLUMN description TEXT;

-- migrate:down
ALTER TABLE job_listings_dev
DROP COLUMN description TEXT;

ALTER TABLE job_listings
DROP COLUMN description TEXT;
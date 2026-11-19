
- Creating the common docker network for services to communicate.
`docker network create job-market-network`

- We then add this to the compose file

```bash
networks:
  job-market-network:
    external: true
```

We created a dedicared postgres role for the app so it can only access its database and not the airflow database. It's basic permission management.

- How to ?

```bash

docker exec -it job-market-postgres \
  sh -lc 'psql -U "$POSTGRES_USER" -d postgres'

CREATE ROLE job_market_app LOGIN;

\password job_market_app


CREATE DATABASE job_market OWNER job_market_app;


\l
\q
```

We migrate using this command

`./db/migrate.py`

It prompts for the migration name then we can write the SQL inside, and run the next following commands.

```bash
status
migrate
status
```


- Copy the content of the prod table into dev table

```sql
BEGIN;


INSERT INTO job_listings_dev (
        source,
        source_guid,
        title,
        company_name,
        raw_data,
        fetched_at,
        is_expired
    )
    SELECT
        source,
        source_guid,
        title,
        company_name,
        raw_data,
        fetched_at,
        is_expired
    FROM job_listings

ON CONFLICT (source, source_guid) DO NOTHING;

COMMIT;
```
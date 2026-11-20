import os
from collections.abc import Iterable

import psycopg
from dotenv import load_dotenv
from psycopg import Connection
from psycopg.types.json import Jsonb

from ..core.exceptions import MissingEnvironmentVariable
from .models import Job
from .tables import JOB_LISTINGS_TABLE, JOB_LISTINGS_TABLE_DEV


class JobMarketDatabase:
    def __init__(self):
        load_dotenv("app.env")

        self.db_url = os.getenv("DATABASE_URL")
        if self.db_url is None:
            raise MissingEnvironmentVariable("DATABASE_URL variable is not set.")

        is_prod_mode = os.getenv("PROD_MODE", "false").lower() == "true"
        self.job_listings_table = (
            JOB_LISTINGS_TABLE if is_prod_mode else JOB_LISTINGS_TABLE_DEV
        )
        print("PROD MODE:", is_prod_mode)

        self.__test_connection()
        self.conn = self._get_connection()

    def __test_connection(self):
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(f"""
                    SELECT * FROM {self.job_listings_table}
                    LIMIT 1;
                """)

    def _get_connection(self) -> Connection:
        return psycopg.connect(self.db_url)

    def _get_upsert_query(self) -> str:
        # When a conflict occurs, Postgres provides the conflicted values through
        # EXCLUDED. We can then take these values to decide what should be updated
        return f"""
        INSERT INTO {self.job_listings_table} AS existing
        (source, source_guid, title, company_name, is_expired, description, raw_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        
        ON CONFLICT (source, source_guid)
        DO UPDATE SET
            title = EXCLUDED.title,
            company_name = EXCLUDED.company_name,
            is_expired = EXCLUDED.is_expired,
            description = EXCLUDED.description,
            raw_data = EXCLUDED.raw_data,
            updated_at = NOW()
        
        WHERE
            existing.title IS DISTINCT FROM EXCLUDED.title OR
            existing.company_name IS DISTINCT FROM EXCLUDED.company_name OR
            existing.is_expired IS DISTINCT FROM EXCLUDED.is_expired OR
            existing.description IS DISTINCT FROM EXCLUDED.description OR
            existing.raw_data IS DISTINCT FROM EXCLUDED.raw_data

        RETURNING (xmax = 0) AS inserted;
        """

    def _job_to_params(self, job: Job) -> tuple:
        return (
            job.source,
            job.source_guid,
            job.title,
            job.company_name,
            job.is_expired,
            Jsonb(job.raw_data),
        )

    def upsert_job(self, job: Job) -> int:
        """
        Insert or update a Job instance in database but does
        not close the connection.
        """

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    self._get_upsert_query(),
                    self._job_to_params(job),
                )
                results = cur.fetchall()

                inserted = sum(1 for row in results if row[0])
                updated = sum(1 for row in results if not row[0])

            self.conn.commit()
            return inserted, updated
        except Exception:
            self.conn.rollback()
            # Raise the exception that just been catched
            raise

    def upsert_batch_jobs(self, jobs: Iterable[Job]) -> int:
        """
        Insert or update a batch of Job instances in database but does
        not close the connection
        """

        params = [self._job_to_params(job) for job in jobs]

        try:
            with self.conn.cursor() as cur:
                cur.executemany(self._get_upsert_query(), params, returning=True)

                results = cur.fetchall()
                inserted = sum(1 for row in results if row[0])
                updated = sum(1 for row in results if not row[0])

            self.conn.commit()
            print("Batch results:", inserted, "inserted", updated, "updated")
            return inserted, updated

        except Exception:
            self.conn.rollback()
            # Raise the exception that just been catched
            raise

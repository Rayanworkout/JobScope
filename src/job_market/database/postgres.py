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

        self.job_listings_table = (
            JOB_LISTINGS_TABLE
            if os.getenv("PROD_MODE", "false").lower() == "true"
            else JOB_LISTINGS_TABLE_DEV
        )

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

    def insert_or_ignore_job(self, job: Job) -> int:
        """
        Insert a Job instance in database but does
        not close the connection.
        """
        query = f"""
            INSERT INTO {self.job_listings_table}
            (source, source_guid, title, company_name, is_expired, raw_data)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (source, source_guid) DO NOTHING;
        """

        params = (
            job.source,
            job.source_guid,
            job.title,
            job.company_name,
            job.is_expired,
            Jsonb(job.raw_data),
        )

        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                inserted = cur.rowcount

            self.conn.commit()
            return inserted

        except Exception:
            self.conn.rollback()
            raise

    def insert_or_ignore_batch_jobs(self, jobs: Iterable[Job]) -> int:
        """
        Insert a batch of Job instances in database but does
        not close the connection
        """
        query = f"""
            INSERT INTO {self.job_listings_table}
            (source, source_guid, title, company_name, is_expired, raw_data)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (source, source_guid) DO NOTHING;
        """

        params = [
            (
                job.source,
                job.source_guid,
                job.title,
                job.company_name,
                job.is_expired,
                Jsonb(job.raw_data),
            )
            for job in jobs
        ]

        try:
            with self.conn.cursor() as cur:
                cur.executemany(query, params)
                inserted = cur.rowcount
            self.conn.commit()
            return inserted
        except Exception:
            self.conn.rollback()
            # Throw again the Exception that has just been captured
            raise

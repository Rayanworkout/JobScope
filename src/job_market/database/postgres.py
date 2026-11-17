import os

import psycopg
from dotenv import load_dotenv
from psycopg import Connection
from psycopg.types.json import Jsonb

from ..core.exceptions import MissingEnvironmentVariable
from .models import Job
from .tables import JOB_LISTINGS_TABLE


class JobMarketDatabase:
    def __init__(self):
        load_dotenv("app.env")
        self.db_url = os.getenv("DATABASE_URL")
        if self.db_url is None:
            raise MissingEnvironmentVariable("DATABASE_URL variable is not set.")

        self.__test_connection()

    def __test_connection(self):
        conn = self._get_connection()
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM {JOB_LISTINGS_TABLE}
                LIMIT 1;
            """)

    def _get_connection(self) -> Connection:
        return psycopg.connect(self.db_url)

    def insert_job(self, job: Job) -> bool:
        conn = self._get_connection()

        with conn, conn.cursor() as cur: # combine with statements
            cur.execute(
                f"""
                    INSERT INTO {JOB_LISTINGS_TABLE}
                    (source, source_guid, title, company_name, is_expired, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (source, source_guid) DO NOTHING;
                    """,
                (
                    job.source,
                    job.source_guid,
                    job.title,
                    job.company_name,
                    job.is_expired,
                    Jsonb(job.raw_data),
                ),
            )

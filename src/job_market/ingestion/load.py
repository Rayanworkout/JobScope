from ..database.postgres import JobMarketDatabase
from .extract import run_extraction


def load_jobs_into_database(max_iterations: int | None = None) -> int:

    db = JobMarketDatabase()

    inserted_count = 0
    updated_count = 0

    for jobs in run_extraction(max_iterations):
        inserted, updated = db.upsert_batch_jobs(jobs)

        inserted_count += inserted
        updated_count += updated

        print(inserted_count, "job(s) inserted in database.")

    return inserted_count

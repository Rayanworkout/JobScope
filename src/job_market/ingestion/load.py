from ..database.postgres import JobMarketDatabase
from .extract import run_extraction


def load_jobs_into_database() -> int:

    db = JobMarketDatabase()

    inserted_count = 0
    for job in run_extraction():
        db.insert_job(job)
        inserted_count += 1

    print(inserted_count, "jobs inserted in database.")
    return inserted_count

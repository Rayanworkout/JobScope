from ..database.postgres import JobMarketDatabase
from .extract import run_extraction


def load_jobs_into_database(max_iterations: int | None = None) -> int:
    db = JobMarketDatabase()

    inserted_count = 0
    
    for jobs in run_extraction(max_iterations):

        inserted_count += db.insert_or_ignore_batch_jobs(jobs)

        print(inserted_count, "jobs inserted in database.")
    
    return inserted_count

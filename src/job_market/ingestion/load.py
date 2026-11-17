from ..database.postgres import JobMarketDatabase
from .extract import run_extraction


def load_jobs_into_database(max_iterations: int | None = None) -> int:
    print("Starting job extraction.", flush=True)
    jobs = run_extraction(max_iterations)
    print(f"Extracted {len(jobs)} jobs. Starting database load.", flush=True)
    db = JobMarketDatabase()

    inserted_count = 0
    for job in jobs:
        db.insert_job(job)
        inserted_count += 1

    print(inserted_count, "jobs inserted in database.")
    return inserted_count

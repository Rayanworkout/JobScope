from ..database.postgres import JobMarketDatabase
from .extract import run_extraction

db = JobMarketDatabase()

for job in run_extraction(max_iterations=1):
    success = db.insert_job(job)
    break

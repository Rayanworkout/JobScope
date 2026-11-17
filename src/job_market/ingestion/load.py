from ..database.postgres import JobMarketDatabase
from .extract import run_extraction

db = JobMarketDatabase()

for job in run_extraction():
    db.insert_job(job)

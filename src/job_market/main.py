"""
Entry point for the ingestion pipeline, run locally or by Airflow.

To run it from the `job_market_intelligence` directory.
"""

# uv run --env-file app.local.env -m src.job_market.main

from .ingestion.load import load_jobs_into_database

if __name__ == "__main__":
    inserted_jobs = load_jobs_into_database(max_iterations=1)
    print(f"Total of {inserted_jobs} jobs inserted in database.")

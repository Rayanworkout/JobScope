"""
This file is only used in development. We use it to manually run the entire
pipeline, but in production the DAGs are running the different commands.

This way we can declare dependencies and manage execution of each step instead
of just one script.

To run it from the `job_market_intelligence` directory.

uv run -m src.job_market.main
"""

from src.job_market.ingestion.extract import run_extraction

run_extraction()

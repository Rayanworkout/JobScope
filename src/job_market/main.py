"""
This file is only used in development. We use it to manually run the entire
pipeline, but in production the DAGs are running the different commands.

This way we can declare dependencies and manage execution of each step instead
of just one script.

To run it from the `job_market_intelligence` directory.
"""

# uv run --env-file app.local.env -m src.job_market.main

import src.job_market.ingestion.load

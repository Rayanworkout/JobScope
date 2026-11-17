from ..database.models import Job
from .services.himalayas import fetch_himalayas_listings


def run_extraction(max_iterations: int | None) -> list[Job]:
    return fetch_himalayas_listings(max_iterations)


# Triggered by the DAG
if __name__ == "__main__":
    run_extraction(max_iterations=None)

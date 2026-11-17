from .models import Job
from .services.himalayas import fetch_himalayas_listings


def run_extraction():
    himalayas_job_listings: list[Job] = fetch_himalayas_listings()

    print(himalayas_job_listings[1])


# Triggered by the DAG
if __name__ == "__main__":
    run_extraction()

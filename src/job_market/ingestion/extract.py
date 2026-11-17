from .services.himalayas import fetch_himalayas_listings


def run_extraction():
    himalayas_job_listings: dict = fetch_himalayas_listings()


# Triggered by the DAG
if __name__ == "__main__":
    run_extraction()

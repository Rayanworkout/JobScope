from .services.himalayas import fetch_himalayas_api


def run_extraction():
    fetch_himalayas_api()


# Triggered by the DAG
if __name__ == "__main__":
    run_extraction()

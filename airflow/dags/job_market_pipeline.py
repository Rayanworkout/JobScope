from datetime import datetime

from airflow.providers.docker.operators.docker import DockerOperator  # pyright: ignore[reportMissingImports]
from docker.types import Mount  # pyright: ignore[reportMissingModuleSource]

from airflow import DAG

with DAG(
    # These args will get passed on to each operator
    dag_id="job_market_pipeline",
    description="Job market data pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["job-market"],
) as dag:
    docker_default_args = {
        "image": "job-market-app:dev",
        "docker_url": "unix://var/run/docker.sock",
        "network_mode": "job-market-network",
        "auto_remove": "success",
        "mount_tmp_dir": False,
        "mounts": [
            Mount(
                source="/home/rayan/dev/Projets/job_market_intelligence/app.env",
                target="/app/app.env",
                type="bind",
                read_only=True,
            )
        ],
    }

    extract_jobs = DockerOperator(
        task_id="extract_jobs",
        command=[
            "/app/.venv/bin/python",
            "-m",
            "job_market.ingestion.extract",
        ],
        **docker_default_args,
    )

    load_jobs = DockerOperator(
        task_id="load_jobs",
        command=[
            "/app/.venv/bin/python",
            "-m",
            "job_market.ingestion.load",
        ],
        **docker_default_args,
    )

    extract_jobs >> load_jobs

    # The mount paths are not Jinja template files despite their .env suffix.
    extract_jobs.template_ext = (".sh", ".bash")

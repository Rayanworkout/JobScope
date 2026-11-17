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

    # Extract Job offers from APIs
    extract_jobs = DockerOperator(
        task_id="extract_jobs",
        image="job-market-app:dev",
        command=[
            "/app/.venv/bin/python",
            "-m",
            "job_market.ingestion.extract",
        ],
        docker_url="unix://var/run/docker.sock",
        network_mode="job-market-network",
        auto_remove="success",
        mount_tmp_dir=False,
        # We mount app.env inside the container
        mounts=[
            Mount(
                source="/home/rayan/dev/Projets/job_market_intelligence/app.env",
                target="/app/app.env",
                type="bind",
                read_only=True,
            )
        ],
    )

    # The mount paths are not Jinja template files despite their .env suffix.
    extract_jobs.template_ext = (".sh", ".bash")

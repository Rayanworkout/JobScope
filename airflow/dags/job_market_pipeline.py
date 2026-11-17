from datetime import datetime

from airflow.providers.docker.operators.docker import DockerOperator  # pyright: ignore[reportMissingImports]

from airflow import DAG, task

with DAG(
    dag_id="job_market_pipeline",
    description="Job market data pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["job-market"],
) as dag:

    @task.bash
    def build_image():
        return "cd /path/to/project && docker build -f app/Dockerfile -t job-market-app:dev ."

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
    )

    # The extraction job depends on the image build
    build_image() >> extract_jobs

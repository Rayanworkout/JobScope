from datetime import datetime

from airflow.providers.docker.operators.docker import DockerOperator

from airflow import DAG

with DAG(
    dag_id="job_market_pipeline",
    description="Job market data pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["job-market"],
) as dag:

    extract = DockerOperator(
        task_id="extract_jobs",
        image="job-market-app:dev",
        command=[
            "python",
            "-m",
            "job_market.ingestion.extract",
        ],
        docker_url="unix://var/run/docker.sock",
        network_mode="job_market_default",
        auto_remove="success",
        mount_tmp_dir=False,
    )
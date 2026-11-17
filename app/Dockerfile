# docker build -f app/Dockerfile -t job-market-app:dev .

FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files and source code
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Sync and install the package into the virtual environment
RUN uv sync --frozen --no-dev

ENV PYTHONPATH=/app/src
ENV PATH="/app/.venv/bin:$PATH"

# This command is overriden by the DAG command anyway
CMD ["python", "-m", "job_market.main"]
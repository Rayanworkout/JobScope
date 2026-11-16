# docker build -f app/Dockerfile -t job-market-app:dev .
# docker run --rm job-market-app:dev

FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/src/

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "job_market.main"]
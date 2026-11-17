
- Creating the common docker network for services to communicate.
`docker network create job-market-network`

- We then add this to the compose file

```bash
networks:
  job-market-network:
    external: true
```

Running a specific container

```bash
docker compose \
  --env-file .env \
  --env-file app.env \
  -f airflow/docker-compose.yaml \
  up -d
```

```bash
docker compose \
  --env-file .env \
  --env-file app.env \
  -f postgres/docker-compose.yaml \
  up -d
```

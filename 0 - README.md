# Job market intelligence

Data engineering and ETL pipeline project. The goal is to create a data pipeline using specific tools. Apache Airflow, Data Build Tool (dbt), PostgreSQL, pgvector, semantic search through an embedding model.


We collect job openings and their metadata from one or multiple sources, (I'll start with [Himalayas API](https://himalayas.app/api)). We'll then store them in PostgreSQL and create custom views / logic via dbt (average wage / most looked for skills ...). We also store these listings as vector using pgvector extension to be able later to make a semantic research through natural language without an exact keyword match.



When the pipeline will be fully working, the results will be visible on my portfolio, currently at [rayan.world](https://rayan.world) to showcase some interesting job postings.
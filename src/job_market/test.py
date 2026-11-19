from dataclasses import replace

from psycopg.rows import dict_row

from .database.models import Job
from .database.postgres import JOB_LISTINGS_TABLE_DEV, JobMarketDatabase

db = JobMarketDatabase()


# On fetch une entrée de BDD et on la convertit en objet Job
with db.conn.cursor(row_factory=dict_row) as cur:
    cur.execute(f"""
        SELECT * FROM {JOB_LISTINGS_TABLE_DEV}
        WHERE id = 2
    """)
    data = cur.fetchone()

job = Job.from_db_row(data)

print("Fetched:", job)
# On modifie un des éléments puis on le réinsère en BDD
job = replace(job, title="test_rayan")

print("New version:", job)

row_count = db.insert_or_ignore_job(job)

print(row_count, "row edited.")

with db.conn.cursor(row_factory=dict_row) as cur:
    cur.execute(f"""
        SELECT * FROM {JOB_LISTINGS_TABLE_DEV}
        WHERE id = 2;
    """)
    data = cur.fetchone()

job = Job.from_db_row(data)

print("Currently in db:", job)

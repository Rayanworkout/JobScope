This is the job market app which is ran by Airflow through a docker container, that's why we have the app/Dockerfile.

Airflow does NOT build the image, it just runs the container with an existing image. We need to rebuild the image when we release a new version of the code.

The main file is used for development ONLY.
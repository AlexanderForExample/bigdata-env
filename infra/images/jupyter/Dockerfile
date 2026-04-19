FROM jupyter/minimal-notebook:python-3.11

USER root
RUN pip install --no-cache-dir \
    requests==2.32.3 \
    pandas==2.2.2 \
    sqlalchemy==2.0.32 \
    psycopg2-binary==2.9.9

# Удобно: работать из /work, а репо монтировать туда
WORKDIR /work

USER jovyan

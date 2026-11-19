FROM apache/airflow:2.9.3-python3.10

USER root
RUN apt-get update && apt-get install -y git && apt-get clean

USER airflow

COPY requirements.txt /requirements.txt
# Explicitly constrain dbt Core: unpinned resolution can select an incompatible Fusion prerelease.
RUN pip install --no-cache-dir -r /requirements.txt "dbt-core==1.8.9" "dbt-postgres==1.8.2" \
    && python -c "import importlib.metadata as m; assert m.version('dbt-core') == '1.8.9', m.version('dbt-core'); assert m.version('dbt-postgres') == '1.8.2', m.version('dbt-postgres')" \
    && dbt --version

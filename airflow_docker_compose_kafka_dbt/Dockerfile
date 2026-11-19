FROM apache/airflow:2.9.3-python3.10

USER root
RUN apt-get update && apt-get install -y git && apt-get clean

USER airflow

COPY requirements.txt /requirements.txt

# Install non-dbt requirements in Airflow's Python environment.
# Keep dbt and its dependencies isolated from Airflow's dependency resolver.
RUN grep -v -E '^[[:space:]]*dbt-(core|postgres)[[:space:]]*([=<>!~].*)?$' /requirements.txt > /tmp/airflow-requirements.txt \
    && pip install --no-cache-dir -r /tmp/airflow-requirements.txt

RUN python -m venv /home/airflow/dbt-venv \
    && /home/airflow/dbt-venv/bin/python -m pip install --no-cache-dir "dbt-core==1.8.9" "dbt-postgres==1.8.2" \
    && /home/airflow/dbt-venv/bin/python -c "import importlib.metadata as m; assert m.version('dbt-core') == '1.8.9'; assert m.version('dbt-postgres') == '1.8.2'"

ENV PATH="/home/airflow/dbt-venv/bin:${PATH}"

RUN dbt --version

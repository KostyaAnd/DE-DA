FROM python:3.8.13

RUN pip install --user psycopg2-binary==2.9.3 apache-airflow==2.3.0 clickhouse-driver==0.2.3 psycopg2==2.9.3 redis==4.3.1 requests==2.27.1

WORKDIR /usr/local/airflow
ENV AIRFLOW_HOME=/usr/local/airflow
ENV PATH=/root/.local/bin:$PATH

COPY ./airflow.cfg /usr/local/airflow/airflow.cfg

from apache/superset

USER root

RUN superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin

RUN superset db upgrade
RUN superset init

RUN pip install clickhouse-driver==0.2.0 && pip install clickhouse-sqlalchemy==0.1.6


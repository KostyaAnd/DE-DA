# Копирование на сервак:
scp -r /Users/ruaavd7/Documents/study/de10-newprolab/labs/lab05 de10-click:/home/ubuntu

# запуск шарманки:
cd ~/lab05/airflow
sudo docker-compose up

# Перезапуск дагов в прошлом (запуск из контейнера с Airflow)
docker exec -it airflow_airflow-webserver_1 bash


airflow dags backfill --start-date 2020-11-21 lab05

airflow dags backfill --start-date 2020-11-22 lab05

airflow dags backfill --start-date 2020-11-23 lab05

airflow dags backfill --start-date 2020-11-24 lab05

airflow dags backfill --start-date 2020-11-25 lab05

airflow dags backfill --start-date 2020-11-26 lab05



airflow dags backfill \
    --start-date 2020-11-21 \
    --end-date 2020-11-26 \
    lab05

## Запросы в клик:
select toDateTime(timestamp) from default.lab_05_events order by 1;

│   2020-11-22 21:56:43 │
│   2020-11-22 21:56:47 │
│   2020-11-22 21:56:52 │
│   2020-11-22 21:57:17 │
│   2020-11-22 21:57:26 │
│   2020-11-22 21:57:39 │


select FROM_UNIXTIME(toInt64(timestamp)) from default.lab_05_events order by 1;

│               2020-11-22 21:56:47 │
│               2020-11-22 21:56:52 │
│               2020-11-22 21:57:17 │
│               2020-11-22 21:57:26 │
│               2020-11-22 21:57:39 │

### Получение списка ключей 
docker exec -it airflow_redis_1 bash
redis-cli
KEYS *

### Получить список значений в наборе данных:
SMEMBERS fav:level2:2020-11-21:23h:top5
SMEMBERS fav:level2:2020-11-22:00h:top5


ZRANGE user:adb7370f-d9fa-4642-8de7-2039cf53e8ce:view:level3:2020-11-21:23h:top10 0 -1 WITHSCORES

ZRANGE user:04a3be61-9800-4116-bfb9-ae8a907821ad:view:level3:2020-11-21:23h:top10 0 -1 WITHSCORES

ZRANGE user:4affe789-48c1-4799-bf73-a376dbb27750:fav:level3:2020-11-21:23h:top5 0 -1 WITHSCORES




## 
docker run --net=host -it -e NPL_REDIS=localhost:6379 shrimpsizemoose/npl-check-lab5:1.0.0



fav:level2:2020-11-23:18h:top5


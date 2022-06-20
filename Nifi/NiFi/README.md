
---------------------ЗАДАЧА------------------------------------------------

С использованием тестовых данных из присланного архива, сделать следующее: 

    1) На Windows или Linux установить: 
        a. MySQL или любую другую СУБД;
        b. Apache NiFi;
    2) Используя NiFi, создать трансформацию, которая в уже существующую таблицу (ее можно сделать вручную с помощью create table из SQL клиента) сделает insert записей из CSV по столбцам;
    3) Прислать шаблон (template) трансформации, по желанию сопроводить отчетом в свободной форме не более 2 листов A4.


-----------------КРАТКОЕ ОПИСАНИЕ РЕШЕНИЯ----------------------------------------

1) Для данной задачи поднял контейнеры с POSTGRES и Ni-fi

2) Создал в БД таблицу с колонками из CSV файла

3) Настроил пайп в nifi



--------------------------Решение--------------------------------------


sudo docker run --name test-pg -e POSTGRES_PASSWORD=Zasadazasada1 -d postgres

sudo docker pull apache/nifi

sudo docker run --name nifi \
    -p 8443:8443 \
    -e SINGLE_USER_CREDENTIALS_USERNAME=admin \
    -e SINGLE_USER_CREDENTIALS_PASSWORD=Zasadazasada1 \
    apache/nifi
    
https://localhost:8443/nifi

sudo docker exec -it test-pg bash

psql --username=postgres --dbname=postgres

CREATE TABLE sales (
    store	   VARCHAR(80),
    check_number   VARCHAR(40),
    check_date     TIMESTAMP,
    amount	   INT,
    price          MONEY, 
    summa	   MONEY,
    serial_id      INT,
    employee_id    VARCHAR(80),
    summa_balov    INT,
    bonus_card     VARCHAR(80),
    check_type     VARCHAR(40),
    str_type_dirr  VARCHAR(40)
);


sudo docker exec -it 32bc7d9c5cb1 bash

mkdir csv

sudo docker cp 1.csv 32bc7d9c5cb1:/opt/nifi/nifi-current/csv

mkdir jdbc

sudo docker cp postgresql-42.4.0.jar nifi:/opt/nifi/nifi-current/docs/jdbc



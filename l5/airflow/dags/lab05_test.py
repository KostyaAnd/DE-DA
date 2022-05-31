import pendulum
import contextlib
import psycopg2
import os
import requests

from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context

import clickhouse_driver
import redis

redis = redis.Redis(host='redis')
click_client = clickhouse_driver.Client.from_url('clickhouse://default:default@194.58.107.61:9090/default')
#click_client = clickhouse_driver.Client(host='194.58.107.61', port=9090)

DEFAULT_ARGS = {"owner": "newprolab"}
TREE_FILE_TEMPLATE = '/tmp/tree_data_{}.csv'


@dag(
    default_args=DEFAULT_ARGS,
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2020, 11, 22),
    catchup=False,
)
def lab05():
    @task
    def update_click_catalog():
        context = get_current_context()
        sql_query = '''
       with recursive cte_catalog as (
            select 
                cat as cat_id 
                , id as row_id
                , parent_id as parent_row_id
                , 0 as parent_cat_id
                , 0 as cat_level
                , '0' as cat_path
            from public.category_tree 
            where cat = 0
            union
            select 
                cat as cat_id 
                , id as row_id
                , parent_id as parent_row_id
                , cc.cat_id as parent_cat_id
                , cc.cat_level + 1 as cat_level
                , cat_path || '-' || cat::text as cat_path
            from public.category_tree ct
            inner join cte_catalog cc on cc.row_id = ct.parent_id 
        )
        , cte_catalog_dedup as (
        	select * from (
	        	select 
	        		c.*
	        		, row_number() over(partition by cat_id order by row_id desc) as rn
	        	from cte_catalog c
        	) t
        	where t.rn = 1
        )   
        select 
            cat_level
            , cat_id
            , parent_cat_id
            , sku_id
            , cat_path
            , split_part(cat_path, '-', 1) as lvl_0_cat
            , split_part(cat_path, '-', 2) as lvl_1_cat
            , split_part(cat_path, '-', 3) as lvl_2_cat
            , split_part(cat_path, '-', 4) as lvl_3_cat
            , split_part(cat_path, '-', 5) as lvl_4_cat
        from cte_catalog_dedup cc
        inner join public.sku_cat sc on sc.cat = cc.cat_id
        '''

        outputquery = "COPY ({0}) TO STDOUT WITH CSV".format(sql_query)
        TREE_FILE_TEMPLATE = '/tmp/npl-de10-lab05-catalog_{}.csv'
        CATALOG_FILENAME = TREE_FILE_TEMPLATE.format(context["dag_run"].run_id)

        CLICKHOUSE_IP = '194.58.107.61'
        CLICKHOUSE_API_PORT = '8123'
        CLICKHOUSE_FULL_URL = f"http://default:default@{CLICKHOUSE_IP}:{CLICKHOUSE_API_PORT}"
        CLICKHOUSE_TBL_NAME = "default.lab_05_category_tree_flat"

        ### Скачивание свежего файла с данными
        with contextlib.closing(
            psycopg2.connect(
            database="sku_info",
            user="lab05",
            password="zua0ieMahk9Jei",
            #host="data.ijklmn.xyz",
            host="85.217.171.166"
            )
        ) as conn:
            cur = conn.cursor()
            with open(CATALOG_FILENAME, 'w') as f:
                cur.copy_expert(outputquery, f)

        ### Транкейт данных в клике
        requests.post(CLICKHOUSE_FULL_URL, data=f"truncate table {CLICKHOUSE_TBL_NAME}")

        ### Проливка данных в клик
        load_data_command = f"cat {CATALOG_FILENAME} | curl '{CLICKHOUSE_FULL_URL}/?query=INSERT%20INTO%20{CLICKHOUSE_TBL_NAME}%20FORMAT%20CSV' --data-binary @-"
        os.system(load_data_command)
        print(load_data_command)  

    @task
    def agg_fav_top5_counts():
        context = get_current_context()
        now, start, end = context["logical_date"], context["data_interval_start"], context["data_interval_end"]

        query = f"""
        with cte as (
            select 
                action_hour
                , lvl_2_cat
                , count(*) as cnt
                , min(timestamp) as first_ts
                , row_number() over(partition by action_hour order by cnt desc, first_ts) as rn
            from default.lab05_events_join_catalog_v
            where action = 'favAdd'
            and action_year = {start.year}
            and action_month = {start.month}
            and action_day = {start.day}
            group by action_hour, lvl_2_cat
        )
        select action_hour, lvl_2_cat from cte where rn <= 5
        """

        print(f"SQL QUERY TO EXECUTION: {query}")
        
        # Получаем данные из клика
        result = click_client.execute(query)

        # Создаем переменную в которй будем хранить последний обработанный ключ
        last_key = ""

        # пробегаемся по результатам запороса клика
        for res_row in result:
            # получаем час и категорию, формируем значение ключа
            action_hour = res_row[0]
            lvl_2_cat = res_row[1]
            key = f"fav:level2:{start.year}-{start.month}-{start.day}:{action_hour:02d}h:top5"

            # если значение ключа изменилось, то обновим last_key и удалим старое значение
            if last_key != key:
                last_key = key
                redis.delete(key)
                print(f"Set {key} was deleted!")

            redis.sadd(key, lvl_2_cat)
            print(f"Category value {lvl_2_cat} added to set {key}")

  
    update_click_catalog() >> agg_fav_top5_counts() 

actual_dag = lab05()

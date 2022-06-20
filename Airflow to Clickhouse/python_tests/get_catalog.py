import contextlib
import psycopg2
import os
import requests

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
from cte_catalog cc
inner join public.sku_cat sc on sc.cat = cc.cat_id
'''

outputquery = "COPY ({0}) TO STDOUT WITH CSV".format(sql_query)
TREE_FILE_TEMPLATE = '/tmp/npl-de10-lab05-catalog_{}.csv'
CATALOG_FILENAME = TREE_FILE_TEMPLATE.format('some_dag_run_id')

CLICKHOUSE_IP = '185.86.146.155'
CLICKHOUSE_API_PORT = '8123'
CLICKHOUSE_FULL_URL = f"http://{CLICKHOUSE_IP}:{CLICKHOUSE_API_PORT}"
CLICKHOUSE_TBL_NAME = "default.lab_05_category_tree_flat"

### Скачивание свежего файла с данными
with contextlib.closing(
    psycopg2.connect(
       database="sku_info",
       user="lab05",
       password="zua0ieMahk9Jei",
       host="data.ijklmn.xyz",
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
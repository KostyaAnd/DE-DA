import requests
import psycopg2


conn = psycopg2.connect("dbname=posts user=postgres password=Zasadazasada1")

cur = conn.cursor()

user_ids = set()

sql_stg_bulk = "INSERT INTO stg.post (user_id, id, title, body) VALUES "  
stg_bulk_list = []

sql_dds_hub_post_bulk = "INSERT INTO dds.hub_post (post_hash_key) VALUES "  
dds_bulk_hub_post_list = []

sql_dds_lnk_post_user_bulk = "INSERT INTO dds.lnk_post_user (post_hash_key, user_hash_key) VALUES "  
dds_bulk_lnk_post_user_list = []

sql_dds_sat_post_bulk = "INSERT INTO dds.sat_post (post_hash_key, title, body) VALUES "  
dds_bulk_sat_post_list = []


r = requests.get('https://jsonplaceholder.typicode.com/posts/')
for row in r.json():
	post_hash_key_str = f"{row['userId']}_{row['id']}"
	stg_bulk_list.append(f"({row['userId']}, {row['id']}, '{row['title']}', '{row['body']}')")
	dds_bulk_hub_post_list.append(f"(MD5('{post_hash_key_str}'))")
	dds_bulk_lnk_post_user_list.append(f"(MD5('{post_hash_key_str}'), MD5('{row['userId']}'))")
	dds_bulk_sat_post_list.append(f"(MD5('{post_hash_key_str}'), '{row['title']}', '{row['body']}')")

	user_ids.add(row['userId']) 


stg_bulk_concat = ",".join(stg_bulk_list)
cur.execute(sql_stg_bulk + stg_bulk_concat)

dds_hub_post_bulk_concat = ",".join(dds_bulk_hub_post_list)
cur.execute(sql_dds_hub_post_bulk + dds_hub_post_bulk_concat)

dds_lnk_post_user_bulk_concat = ",".join(dds_bulk_lnk_post_user_list)
cur.execute(sql_dds_lnk_post_user_bulk + dds_lnk_post_user_bulk_concat)

dds_sat_post_bulk_concat = ",".join(dds_bulk_sat_post_list)
cur.execute(sql_dds_sat_post_bulk + dds_sat_post_bulk_concat)

sql_dds_hub_user_bulk = "INSERT INTO dds.hub_user (user_hash_key) VALUES "  
dds_bulk_hub_user_list = []

for user_id in user_ids:
	dds_bulk_hub_user_list.append(f"(MD5('{user_id}'))")

dds_hub_user_bulk_concat = ",".join(dds_bulk_hub_user_list)
cur.execute(sql_dds_hub_user_bulk + dds_hub_user_bulk_concat)


conn.commit()
cur.close()
conn.close()
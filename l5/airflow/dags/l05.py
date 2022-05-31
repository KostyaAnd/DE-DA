import redis
from clickhouse_driver import Client
import datetime
import pandas as pd
r = redis.StrictRedis(host='localhost', port=6379, db=0)
print(f'Очистка {r.flushall()}')
print(r.mset({'myset2':str(datetime.datetime.now())}) )
print(r.get("myset2"))
rehydrated_df = r.smembers("myset")
print(rehydrated_df)
print("1364:2030-01-09:03h:top10")
client = Client(host='localhost')
query2="""
select *
from (select row_number()over(partition by toStartOfHour(FROM_UNIXTIME(toUInt64(a.timestamp))) order by count(*) desc,min(FROM_UNIXTIME(toUInt64(a.timestamp))) asc) rn
            ,substr(b.lv3,5,2)cat
            ,toStartOfHour(FROM_UNIXTIME(toUInt64(a.timestamp))) tm
            ,count(*)c
            ,min(FROM_UNIXTIME(toUInt64(a.timestamp)) )m
      from a
      join (SELECT * FROM postgresql('data.ijklmn.xyz:5432', 'sku_info', 'vv', 'lab05', 'zua0ieMahk9Jei'))b on substr(a.itemId,5,100)=b.sku_id
      where action='favAdd'
            --and toStartOfHour(FROM_UNIXTIME(toUInt64(a.timestamp)))='2020-11-22 01:00:00'
      group by substr(b.lv3,5,2), toStartOfHour(FROM_UNIXTIME(toUInt64(a.timestamp)))
      )
where rn<6
--order by c desc,m asc
"""
print(f'query sql {query2}')
got_sql=client.execute(query2)
print(pd.DataFrame(got_sql))
for i in got_sql:
    hour = i[2].strftime('%H')
    day = i[2].day
    month = i[2].month
    year = i[2].year
    cat = i[1]
    print(f'fav:level2:{year}-{month}-{day}:{hour}h:top5 {cat}')
    r.sadd(f'fav:level2:{year}-{month}-{day}:{hour}h:top5',f'{cat}')
    #print('--')
    print(r.smembers(f'fav:level2:{year}-{month}-{day}:{hour}h:top5'))
        #print(r.smembers("myset"))
    print("-------------------------------------------------------------")

--------- DDL для таблицы каталога:
DROP TABLE default.lab_05_category_tree_flat;

CREATE TABLE default.lab_05_category_tree_flat
(
cat_level Int32
, cat_id Int32
, parent_cat_id Int32
, sku_id String
, cat_path String
, lvl_0_cat Int32
, lvl_1_cat Int32
, lvl_2_cat Int32
, lvl_3_cat Int32
, lvl_4_cat Int32
) ENGINE = MergeTree()
  PRIMARY KEY cat_id
  ORDER BY cat_id
  SETTINGS index_granularity = 8192;


DROP TABLE default.lab_05_events;

CREATE TABLE default.lab_05_events
(
userId String
, itemId String
, action String
, timestamp Float64
) ENGINE = MergeTree()
  PRIMARY KEY timestamp
  ORDER BY timestamp
  SETTINGS index_granularity = 8192;


create or replace view default.lab05_events_formatted_v as 
select 
	toUUID(splitByString(':', userId)[2]) as userId
	, toUUID(splitByString(':', itemId)[2]) as itemId
	, action
  , timestamp
	, toDateTime(timestamp) as action_dt
	, toDate(action_dt) as action_date
	, toYear(action_dt) as action_year
	, toMonth(action_dt) as action_month
	, toDayOfMonth(action_dt) as action_day
	, toHour(action_dt) as action_hour
from default.lab_05_events;


create or replace view default.lab05_events_join_catalog_v as 
select 
    userId
    , itemId
    , lvl_2_cat
    , lvl_3_cat
    , action
    , timestamp
    , action_dt
    , action_date
    , action_year
    , action_month
    , action_day
    , action_hour
from default.lab05_events_formatted_v as e
inner join default.lab_05_category_tree_flat as c on e.itemId = toUUID(c.sku_id);

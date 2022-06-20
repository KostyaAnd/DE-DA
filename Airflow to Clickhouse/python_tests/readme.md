# Установка и активация виртуального окружения:
virtualenv env -p 3.8
source env/bin/activate

### отключение виртуального окружения
deactivate

# Установка пакетов:
pip install -r requirements.txt --index-url https://pypi.python.org/simple

#

truncate table default.lab_05_category_tree_flat;
truncate table default.lab_05_events;

cat ~/Downloads/tech_events_from_github.jsonl | curl 'http://185.86.146.155:8123/?query=INSERT%20INTO%20default.lab_05_events%20FORMAT%20JSONEachRow' --data-binary @-

select count(*) from default.lab_05_events;  -- 110000

cat ~/Downloads/tech_events_from_garik.jsonl | curl 'http://185.86.146.155:8123/?query=INSERT%20INTO%20default.lab_05_events%20FORMAT%20JSONEachRow' --data-binary @-

select count(*) from default.lab_05_events;  -- 100000













cat resultsfile.csv | curl 'http://185.86.146.155:8123/?query=INSERT%20INTO%20default.lab_05_category_tree_flat%20FORMAT%20CSV' --data-binary @-




cat /tmp/lab05_test.json | curl 'http://185.86.146.155:8123/?query=INSERT%20INTO%20default.lab_05_events%20FORMAT%20JSONEachRow' --data-binary @-

cat /tmp/lab_05_one_row.json | curl 'http://185.86.146.155:8123/?query=INSERT%20INTO%20default.lab_05_events%20FORMAT%20JSONEachRow' --data-binary @-
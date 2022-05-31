from flask import Flask
from flask import request, make_response, jsonify
import requests
from prometheus_flask_exporter import PrometheusMetrics

LAB_04_CONFIG = {
  "NPL_KAFKA": "95.163.213.92:6667",
  "NPL_TOPIC": "dmitry_andreev_lab04_in",
  "NPL_CLICKHOUSE_URL": "185.86.146.155:8123",
  "NPL_CLICKHOUSE_DESTINATION_TABLE": "dmitry_andreev_lab04",
}
NPL_CLICKHOUSE_URL_HTTP = f"http://{LAB_04_CONFIG['NPL_CLICKHOUSE_URL']}"

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/lab04-config')
def lab_config():
    return jsonify(LAB_04_CONFIG)

@app.route('/health')
def health_check():
    r = requests.get(NPL_CLICKHOUSE_URL_HTTP)
    is_click_ok = True if r.status_code == 200 and r.text == 'Ok.\n' else False
    return {"message": "I'm alive!", "click_ok": is_click_ok}

@app.route('/clean-mv', methods=['POST'])
def clean_mv():
    status_code = 200
    result_text = 'Table default.dmitry_andreev_lab04 truncated!'
    try:
        r = requests.post(NPL_CLICKHOUSE_URL_HTTP, data="truncate table default.dmitry_andreev_lab04")
    except:
        result_text = 'Чет ошибочка вышла...'
        status_code = 500
    return make_response(
        jsonify({'status': status_code, 'result': result_text}),
        status_code,
    )

@app.route('/do_something/<int:my_param>', methods=['POST'])
def do_something(my_param):
    return(f"PARAMETER {my_param}\nPOST DATA: {request.json}\n")

@app.route('/compute-aggs', methods=['GET'])
def compute_aggs():
    fields = request.args.get('fields')
    start_ts = request.args.get('start_ts')
    end_ts = request.args.get('end_ts')

    fields_sql = "revenue,visitors,purchases,aov"
    start_ts_sql = f" AND timestamp >= {start_ts}" if start_ts is not None else ""
    end_ts_sql = f" AND timestamp <= {end_ts}" if end_ts is not None else ""

    sql = f'''
with cte as (
    select 
        sum(case when eventType = 'itemBuyEvent' then item_price else 0 end) as revenue
        , count(distinct partyId) as visitors
        , count(distinct case when eventType = 'itemBuyEvent' then sessionId else null end) as purchases
        , case when purchases > 0 then round(revenue / purchases, 1) else 0 end as aov
    from default.dmitry_andreev_lab04
    where detectedDuplicate = false and detectedCorruption = false 
    {start_ts_sql}
    {end_ts_sql}
)
select {fields_sql} from cte    
    '''
    r = requests.get(NPL_CLICKHOUSE_URL_HTTP, params={'query': sql})
    fields_str = fields if fields is not None else fields_sql
    resp_list = r.text.split()
    fields_list = fields_str.split(",")
    
    resp_dictionary_str = dict(zip(fields_sql.split(","), resp_list))
    resp_dictionary_all = dict()
    resp_dictionary_all["revenue"] = int(resp_dictionary_str["revenue"])
    resp_dictionary_all["visitors"] = int(resp_dictionary_str["visitors"])
    resp_dictionary_all["purchases"] = int(resp_dictionary_str["purchases"])
    resp_dictionary_all["aov"] = float(resp_dictionary_str["aov"])
    
    print(resp_dictionary_all)

    resp_dictionary = {k: resp_dictionary_all[k] for k in fields_list}

    print(resp_dictionary)

    return(jsonify(resp_dictionary))

@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'status': 404, 'error': 'path not found'}),
        404,
    )



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

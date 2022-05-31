from crypt import methods
from distutils.command.clean import clean
from email.policy import default
from os import truncate
from wsgiref.util import request_uri
from flask import request, make_response, jsonify, Flask
import requests
from clickhouse_driver import Client

LAB_04_CONF = {
  "NPL_KAFKA": "kafka.ijklmn.xyz:9092",
  "NPL_TOPIC": "konstantin_andreev_lab04_in",
  "NPL_CLICKHOUSE_URL": "5.188.141.0:8123",
  "NPL_CLICKHOUSE_DESTINATION_TABLE": "konstantin_andreev_lab04",
}

click_url = 'http://5.188.141.0:8123'

app = Flask(__name__)

@app.route('/health')
def health_check():
    req = requests.get(click_url)
    is_click_ok = req.status_code == 200
    return jsonify({"message": "I'm alive!", "click_ok": is_click_ok})

@app.route('/lab04-config')
def lab_conf():
    return jsonify(LAB_04_CONF)

@app.route('/clean-mv',  methods=['POST'])
def clean_mat_view():
    requests.post(click_url, data="truncate table default.konstantin_andreev_lab04")
    return "OK"

@app.route('/compute-aggs')
def compute_aggs():
    fields = request.args.get('fields')
    start_ts = request.args.get('start_ts')
    end_ts = request.args.get('end_ts')
    
    start_ts_sql = f"AND timestamp >= {start_ts}" if start_ts is not None else ""
    end_ts_sql = f"AND timestamp <= {end_ts}" if end_ts is not None else ""


    sql = f''' WITH CTE AS (
        SELECT SUM (item_price) AS revenue,
        count (DISTINCT sessionId) AS purchases,
        CASE WHEN purchases > 0 THEN ROUND(revenue / purchases, 1) ELSE 0 END AS aov 
        FROM konstantin_andreev_lab04
        WHERE detectedDuplicate = false AND detectedCorruption = false AND eventType = 'itemBuyEvent' 
        {start_ts_sql}
        {end_ts_sql}
    )
    SELECT {fields}
    FROM CTE '''

    client = Client('5.188.141.0',port=9090)
    result = client.execute(sql)
    return jsonify(dict(zip(fields.split(","), result[0])))

@app.route('/do_something/<int:my_param>', methods=['POST'])
def do_something(my_param):
    return(f"PARAMETER {my_param}\nPOST DATA: {request.json}\n")

@app.route('/params', methods=['GET'])
def do_something_with_params():
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    return(f"PARAM1 {param1} PARAM2 {param2}\n")

@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'status': 404, 'error': 'path not found'}),
        404,
    )
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    

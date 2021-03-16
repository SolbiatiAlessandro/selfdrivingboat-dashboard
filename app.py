from flask import Flask, url_for,redirect,request,render_template
import time
import sys
import datetime
import logging
import influxdb_query
app = Flask(__name__)

states = ["DEFAULT", "FORWARD", "LEFT", "RIGHT", "STOP"]
STATE = 1

@app.route('/ping', methods=['POST'])
def ping_from_boat():
    data = request.form
    if data.get('source') is not None and data['source'] == "1kgboat":
        print("GOT A PING FROM THE BOAT!")
        logging.warning("GOT A PING FROM THE BOAT")
    return "received"

@app.route('/influx_db_updated')
def influxdb_updated():
    print(request.args)
    last_ts = request.args.get('last_ts', '', str)
    query_res = influxdb_query.query_from_last_ts(last_ts)
    if query_res:
        return {'updated': True}
    return {'updated': False}

@app.route('/')
def homepage():
    last_ts = request.args.get('last_ts', '', str)
    print("homepage called with last_ts={}".format(last_ts))
    if last_ts == '':
        yesterday = datetime.date.today() - datetime.timedelta(1)
        yesterday_unixtime= yesterday.strftime("%s")
        last_ts = yesterday_unixtime
    query_res = influxdb_query.query_from_last_ts(last_ts)
    influxdb_data = influxdb_query.parse_tables_last_values(query_res)
    print(influxdb_data, flush=True)
    current_unixtime = time.time()
    additional_data = {'unix_ts':current_unixtime}

    return render_template("index.html", **{**influxdb_data, **additional_data})

@app.route('/set_state/<state>')
def set_state(state):
    global STATE
    STATE = states.index(state)
    return redirect('/')

@app.route('/state')
def get_state():
    return states[STATE]

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


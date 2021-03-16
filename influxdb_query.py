# https://github.com/influxdata/influxdb-client-python
import time
import logging
import sys
from influxdb_client import InfluxDBClient
bucket="alessandro.solbiati's Bucket"
token = "L8LEe0QrLQysteAE6-cLLEy8ezz-gOJdO-eRpZ4ugRJdpgNsFy66P0BXlziYjqtRabn-R-4lNsemAatT8xPkqg=="
org = "alessandro.solbiati@gmail.com"
client = InfluxDBClient(url="https://westeurope-1.azure.cloud2.influxdata.com", token=token, org=org)
query_api = client.query_api()

def query_from_last_ts(last_ts):
    if last_ts == '':
        return None
    last_ts = int(float(last_ts))
    current_ts = time.time()
    seconds_delta = int(current_ts - last_ts)
    if seconds_delta == 0:
        seconds_delta = 1
    print("querying influxdb last {} seconds".format(seconds_delta), flush=True)
    tables = query_api.query('from(bucket:"{}") |> range(start: -{}s)'.format(bucket, seconds_delta))
    print(tables, flush=True)
    return tables

def parse_tables_last_values(tables):
    res = {}
    for table in tables:
        r = table.records[-1]
        try:
            key = r['device']+r['_field'] 
            res[key.replace('.', '_')] = r['_value']
            res['time'] = r['_time'].strftime("%s")
        except KeyError as e:
            pass
    return res




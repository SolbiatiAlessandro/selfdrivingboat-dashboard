from flask import Flask, url_for,redirect,request,render_template
import time
import sys
import datetime
import logging
import boto3
import os
import json
app = Flask(__name__)

import influxdb_query
import db
import aws

states = ["", "FORWARD", "LEFT", "RIGHT", "STOP"]
STATE = 0

@app.route('/influx_db_latest_data')
def influxdb_latest_data():
    print(request.args)
    last_ts = request.args.get('last_ts', '', str)

    if last_ts == '':
        yesterday = datetime.date.today() - datetime.timedelta(1)
        yesterday_unixtime= yesterday.strftime("%s")
        last_ts = yesterday_unixtime
    query_res = influxdb_query.query_from_last_ts(last_ts)
    if not query_res:
        return {'updated': False}
    return process_data(query_res)

@app.route('/influx_db_updated')
def influxdb_updated():
    print(request.args)
    last_ts = request.args.get('last_ts', '', str)
    query_res = influxdb_query.query_from_last_ts(last_ts)
    if query_res:
        return {'updated': True}
    return {'updated': False}

@app.route('/read_last_command')
def read_last_command():
    boat_name = request.args.get('boat_name', '', str)

    try:
        boat_accepted_name = os.environ['BOAT_NAME']
    except KeyError:
        with open('boat.secret', 'r') as f:
            boat_accepted_name = f.read()

    if boat_accepted_name not in boat_name:
        return {'command': 'NOT AUTHENTICATED, ?boat_name=XXX'}
    command = db.read_last_command(boat_name)
    return {'command': command}

@app.route('/')
def homepage():
    last_ts = request.args.get('last_ts', '', str)
    print("homepage called with last_ts={}".format(last_ts))
    if last_ts == '':
        yesterday = datetime.date.today() - datetime.timedelta(1)
        yesterday_unixtime= yesterday.strftime("%s")
        last_ts = yesterday_unixtime
    query_res = influxdb_query.query_from_last_ts(last_ts)

    return render_template("index.html", **process_data(query_res))

def process_data(query_res):
    influxdb_data = influxdb_query.parse_tables_last_values(query_res)
    print(influxdb_data, flush=True)

    current_unixtime = time.time()
    last_pic_path = 'static/'+str(current_unixtime)
    aws.get_last_image(last_pic_path)

    additional_data = {'unix_ts':current_unixtime, 'last_pic_path':str(current_unixtime), 'updated': True}
    return {**influxdb_data, **additional_data}

@app.route('/set_command')
def set_command():
  command = request.args.get('command')
  try:
      db.add_new_command(command)
      _time = time.ctime()
      return {'result': 'OK', 'time':_time}
  except Exception as e:
      _time = time.ctime()
      return {'result': e.__str__(), 'time':_time}

@app.route('/sign_s3/')
def sign_s3():
  S3_BUCKET = os.environ.get('S3_BUCKET')
  if not S3_BUCKET:
      S3_BUCKET = 'selfdrivingboatpics'

  file_name = request.args.get('file_name')
  file_type = request.args.get('file_type')

  s3 = boto3.client('s3')

  presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )

  return json.dumps({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

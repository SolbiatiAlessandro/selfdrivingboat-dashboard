from flask import Flask, url_for,redirect,request
from datetime import datetime
import logging
app = Flask(__name__)

states = ["DEFAULT", "FORWARD", "LEFT", "RIGHT", "STOP"]
STATE = 0

@app.route('/ping', methods=['POST'])
def ping_from_boat():
    data = request.form
    if data.get('source') is not None and data['source'] == "1kgboat":
        print("GOT A PING FROM THE BOAT!")
        logging.warning("GOT A PING FROM THE BOAT")
    return "received"

@app.route('/')
def homepage():
    return """
    <div style="padding:30px;border:1px;">CURRENT STATE: {}</div>
    <div style="display:flex">
    <div style="width:80%;padding:10%;background-color:orange;color:white;"><a href="/set_state/FORWARD">FORWARD</a></div>
    <div style="width:80%;padding:10%;background-color:green"><a href="/set_state/LEFT">LEFT</a></div>
    <div style="width:80%;padding:10%;background-color:yellow"><a href="/set_state/RIGHT">RIGHT</a></div>
    <div style="width:80%;padding:10%;background-color:red"><a href="/set_state/STOP">STOP</a></div>
    </div>
    """.format(states[STATE])

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


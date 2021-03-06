from flask import Flask, url_for,redirect
from datetime import datetime
app = Flask(__name__)

states = ["DEFAULT", "FORWARD", "LEFT", "RIGHT", "STOP"]
STATE = 0

@app.route('/')
def homepage():
    return """
    <div style="padding:30px;border:1px;">CURRENT STATE: {}</div>
    <a style="background-color:blue;color:white;" href="/set_state/FORWARD">FORWARD</a>
    <a style="background-color:green" href="/set_state/LEFT">LEFT</a>
    <a style="background-color:yellow" href="/set_state/RIGHT">RIGHT</a>
    <a style="background-color:red" href="/set_state/STOP">STOP</a>
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


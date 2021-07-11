import flask
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/alive', methods=['GET'])
### Says that Server is Ok or not (filter, net problems, etc)
def home():
    uptime = get_uptime()
    res = "Yes! I am Alive :) - " + str(uptime)
    return str(res)

def get_uptime():
    with open('/proc/uptime','r') as f:
        uptime = float(f.readline().split()[0])
        
    return uptime

@app.route('/run', methods=['PUT'])
### Runs commands
def get_info():
    return request.get_json()['command']    # TODO: this func should run light commands


app.run(host='0.0.0.0')

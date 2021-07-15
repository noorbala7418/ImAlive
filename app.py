import os
import json
import subprocess
import re
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True

load_dotenv(find_dotenv(".env"))
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    sys_username = os.getenv("USERNAME")
    sys_password = os.getenv("PASSWORD")

    if username == sys_username and check_password_hash(generate_password_hash(sys_password), password):
        return True
    
    return False


@app.route('/alive', methods=['GET'])
### Says that Server is Ok or not (filter, net problems, etc)
def alive():
    uptime = get_uptime()
    res = json.dumps({'message': f"Yes! I am Alive :)", 'uptime':str(uptime)})
    response = Response(response=res, status=200, mimetype="application/json")
    return (response)


def get_uptime():
### Gets uptime of system
    with open('/proc/uptime', 'r') as f:
        uptime = float(f.readline().split()[0])

    return uptime


@app.route('/service/state/<string:service_name>', methods=['GET'])
@auth.login_required
def show_state_services(service_name):
### Gets Service Status from system.

    service_state = get_service_full_status(service_name)
    
    if service_state.startswith('Error:'):
        srv_not_found = json.dumps({'state': service_state})
        return Response(response=srv_not_found, status=404, mimetype="application/json")
    
    else:
        service_state = get_service_status(service_state)

        res = json.dumps({'state': service_state})

        response = Response(response=res, status=200, mimetype="application/json")
        return (response)


def get_service_status(service_state):
### cleans service status string.

    reg_order = r'(Active:.+)CPU'
    res = re.findall(reg_order,service_state)
    return res


def get_service_full_status(service_name):
### gets service status from system. convets those to string and returns.
    try:
        service_state = str(subprocess.check_output(["systemctl","status",service_name]))
        return service_state
    
    except subprocess.CalledProcessError as e:
        return f'Error: Service {service_name} Not found.'


@app.route('/run', methods=['POST'])
@auth.login_required
### Runs commands
def get_info():
    # TODO: this func should run light commands
    # return request.get_json()['command']
    return {'message':'This EP hasn\'t implemented.'}


@app.route('/', methods=['GET'])
def home():
    return 'Im Alive! application. an easy tool for managing your server :)'    


app.run(host=os.getenv("HOST_URL"), port=os.getenv("HOST_PORT"))

# Import functions and objects the microservice needs.
# - Flask is the top-level application. You implement the application by adding methods to it.
# - Response enables creating well-formed HTTP/REST responses.
# - requests enables accessing the elements of an incoming HTTP/REST request.
#
import json

# Setup and use the simple, common Python logging framework. Send log messages to the console.
# The application should get the log level out of the context. We will change later.
#

import os
import sys
import platform
import socket

from flask import Flask, Response
from flask import request

cwd = os.getcwd()
sys.path.append(cwd)

print("*** PYHTHONPATH = " + str(sys.path) + "***")

import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Create the application server main class instance and call it 'application'
# Specific the path that identifies the static content and where it is.
application = Flask(__name__,
                    static_url_path='/static',
                static_folder='static')




# 1. Extract the input information from the requests object.
# 2. Log the information
# 3. Return extracted information.
#
def log_and_extract_input(method, path_params=None):

    path = request.path
    args = dict(request.args)
    data = None
    headers = dict(request.headers)
    method = request.method

    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        # This would fail the request in a more real solution.
        data = "You sent something but I could not get JSON out of it."

    log_message = str(datetime.now()) + ": Method " + method

    inputs =  {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data
        }

    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)

    return inputs


def log_response(method, status, data, txt):

    msg = {
        "method": method,
        "status": status,
        "txt": txt,
        "data": data
    }

    logger.debug(str(datetime.now()) + ": \n" + json.dumps(msg, indent=2, default=str))




# This function performs a basic health check. We will flesh this out.
@application.route("/api/health", methods=["GET"])
def health_check():

    pf = platform.system()

    rsp_data = { "status": "healthy", "time": str(datetime.now()),
                 "platform": pf,
                 "release": platform.release()
                 }

    if pf == "Darwin":
        rsp_data["note"]= "For some reason, macOS is called 'Darwin'"


    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    rsp_data["hostname"] = hostname
    rsp_data["IPAddr"] = IPAddr

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


@application.route("/demo/<parameter>", methods=["GET", "POST"])
def demo(parameter):

    inputs = log_and_extract_input(demo, { "parameter": parameter })

    msg = {
        "/demo received the following inputs" : inputs
    }

    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp

@application.route("/boo", methods=["GET"])
def boo():
    rsp = Response("Hoo", status=200, content_type="text/plain")
    return rsp


logger.debug("__name__ = " + str(__name__))


@application.route("/api/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def manage_a_user(user_id):
    pass

def myfirstmethod(verb, path, path_params, query_params, headers, body):
    pass

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.

    application.run(host="0.0.0.0", port=8000)
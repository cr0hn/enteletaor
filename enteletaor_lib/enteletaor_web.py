# -*- coding: utf-8 -*-

import json
import os.path

from time import sleep
from threading import Thread

from flask import Flask
from flask_socketio import SocketIO

BASE_RESOURCES = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "web"))

app = Flask(__name__,
            static_folder=os.path.join(BASE_RESOURCES, "static"),
            template_folder=BASE_RESOURCES)

socketio = SocketIO(app)


# --------------------------------------------------------------------------
# End points
# --------------------------------------------------------------------------
@app.route("/")
def home():
    return open(os.path.join(BASE_RESOURCES, "home.html")).read()


@app.route("/convert", methods=["GET", "POST"])
def convert():
    Thread(target=handle_my_custom_event).start()

    # Recive files
    return json.dumps(dict(result="oks!"))


@app.route("/wait", methods=["GET"])
def wait():
    return open(os.path.join(BASE_RESOURCES, "wait.html")).read()


# --------------------------------------------------------------------------
# Actions sent to users
# --------------------------------------------------------------------------
def handle_my_custom_event():

    socketio.emit('finish')

if __name__ == '__main__' and __package__ is None:
    # --------------------------------------------------------------------------
    # INTERNAL USE: DO NOT MODIFY THIS SECTION!!!!!
    # --------------------------------------------------------------------------
    import sys, os
    sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __import__("enteletaor_lib")
    __package__ = str("enteletaor_lib")
    # --------------------------------------------------------------------------
    # END INTERNAL USE
    # --------------------------------------------------------------------------

    socketio.run(app)

#!/usr/bin/python3

from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)


class User:
    def __init__(self, name: str):
        self.name = name


class Channel:
    def __init__(self, name: str, participants: User):
        self.name = name
        self.participants = participants  # do we need a lock on this?
        # todo: add history?

    def add_participant(self, participant: User):
        self.participants.extend(participant)


@app.route("/")
def root():
    return "<p>root</p>"


@sockets.route("/echo")
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


"""
@app.route("/chatserver/<channel_name>")
def hello_world(channel_name):
    channel = Channel(channel_name, [])
    return "<p>Hello, %s!</p>" % channel.name
"""

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

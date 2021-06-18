from flask import Flask, render_template, request
from flask_restful import reqparse, abort, Api, Resource
from flask_socketio import SocketIO
import shell
import io
import threading

app = Flask(__name__)
socketio = SocketIO(app)
shell = shell.Shell(socketio, "pintos -v -k --bochs --disk cs162proj.dsk -- -q run shell")

@app.route('/')
def home():
    return render_template("index.html")

@socketio.on('connect')
def connect():
    #shell.run()
    if not shell.output_thread.isAlive():
        socketio.start_background_task(shell.output)

@socketio.on('disconnect')
def disconnect():
    shell.input("halt\r")

@socketio.on('send_input')
def shell_input(msg, methods=['POST']):
    shell.input(msg + '\r')
    
if __name__ == '__main__':
    shell.run()
    socketio.run(app, host='192.168.162.162', port=8000, debug=False)
    #socketio.run(app, host='0.0.0.0', port=5000, debug=False)

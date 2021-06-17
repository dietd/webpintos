from flask import Flask, render_template, request
from flask_restful import reqparse, abort, Api, Resource
from flask_socketio import SocketIO
import os_listener
import io
import threading

app = Flask(__name__)
socketio = SocketIO(app)
shell = os_listener.Shell(socketio, "pintos -v -k --qemu --disk cs162proj.dsk -- -q run shell")

# This is the function thread calls to output the shell output
def shell_output():
    buf = io.StringIO()
    while True:
        data = shell.p.stdout.read(1)
        if data:
            buf.write(data.decode("utf-8"))
        else:
            if (buf.getvalue() != ""):
                socketio.emit('send_output', buf.getvalue())
                buf = io.StringIO()

thread = threading.Thread()

@app.route('/')
def home():
    return render_template("index.html")

@socketio.on('connect')
def connect():
    shell.run()
    global thread
    if not thread.isAlive():
        thread = socketio.start_background_task(shell_output)

@socketio.on('disconnect')
def disconnect():
    shell.input("halt\r")
    global thread
    thread.join()

@socketio.on('send_input')
def shell_input(msg, methods=['POST']):
    shell.input(msg + '\r')
    
if __name__ == '__main__':
    socketio.run(app, host='192.168.162.162', port=8000, debug=True)

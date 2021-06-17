import subprocess
import threading
import io
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK
import sys
#from flask_socketio import SocketIO

command = "pintos -v -k --qemu --disk cs162proj.dsk -- -q run shell"

class Shell():
    def set_flags(self, pipe):
        flags = fcntl(pipe, F_GETFL)
        fcntl(pipe, F_SETFL, flags | O_NONBLOCK)
    
    def __init__(self, app, command):
        self.app = app
        self.cmd = command

    def run(self):
        self.p = subprocess.Popen(self.cmd.split(' '),
                cwd="./os_build",
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                )
        self.set_flags(self.p.stdout)
        self.set_flags(self.p.stdin)
        #self.output_thread = self.app.start_background_task(self.output)


    def output(self):
        buf = io.StringIO()
        while True:
            data = self.p.stdout.read(1)
            if data:
                #sys.stdout.write(data.decode('utf-8'))
                buf.write(data.decode('utf-8'))
            else:
                if (buf.getvalue() != ""):
                    self.app.emit('send_output', buf.getvalue())
                    buf = io.StringIO()

    def input(self, command):
        self.p.stdin.write(command.encode())
        self.p.stdin.flush()

#shell = Shell(None, command)
#shell.input("ls\r")
#shell.input("mkdir dab_on\r")

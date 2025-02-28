import subprocess
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Replace with your tmux session name
TMUX_SESSION = 'mysession'

# This function sends a command to a tmux window
def send_command_to_tmux(command):
    try:
        # Send the command to the tmux session
        subprocess.run(["tmux", "send-keys", "-t", TMUX_SESSION, command, "C-m"])
    except Exception as e:
        return str(e)
    return "Command sent successfully."

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('run_command')
def handle_run_command(data):
    command = data.get('command')
    if not command:
        emit('output', {"error": "No command provided"})
    else:
        result = send_command_to_tmux(command)
        emit('output', {"data": result})

if __name__ == '__main__':
    socketio.run(app, debug=True)

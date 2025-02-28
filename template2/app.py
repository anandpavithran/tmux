import subprocess
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Define the tmux session name
TMUX_SESSION = 'mysession'

def send_command_to_tmux(command):
    try:
        # Ensure tmux session exists
        result = subprocess.run(['tmux', 'has-session', '-t', TMUX_SESSION], capture_output=True, text=True)
        if result.returncode != 0:
            subprocess.run(['tmux', 'new-session', '-d', '-s', TMUX_SESSION])  # Create session if doesn't exist

        # Send the selected text as a command to the tmux session
        subprocess.run(['tmux', 'send-keys', '-t', TMUX_SESSION, command, 'C-m'])
    except Exception as e:
        return str(e)
    return "Command sent successfully."

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('submit_text')
def handle_submit_text(data):
    selected_text = data.get('text')  # This is the selected text from the webpage
    if not selected_text:
        emit('output', {'error': 'No text selected'})
    else:
        result = send_command_to_tmux(selected_text)
        emit('output', {'result': result})

if __name__ == '__main__':
    socketio.run(app, debug=True)

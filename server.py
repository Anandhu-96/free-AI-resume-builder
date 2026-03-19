import os
import subprocess
import threading
import time
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

streamlit_process = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/start-streamlit', methods=['POST'])
def start_streamlit():
    global streamlit_process
    if streamlit_process and streamlit_process.poll() is None:
        return jsonify({'status': 'already_running', 'url': 'http://localhost:8501'})
    cmd = ['streamlit', 'run', 'page.py', '--server.address', '0.0.0.0', '--server.port', '8501']
    streamlit_process = subprocess.Popen(cmd, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # wait a bit for startup
    for _ in range(25):
        time.sleep(0.2)
        try:
            import urllib.request
            with urllib.request.urlopen('http://localhost:8501', timeout=1) as resp:
                if resp.status == 200:
                    return jsonify({'status': 'started', 'url': 'http://localhost:8501'})
        except Exception:
            continue
    return jsonify({'status': 'started', 'url': 'http://localhost:8501'})

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(port=8000, debug=False)

from flask import Flask, jsonify, render_template
import json
import subprocess
import atexit

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/surebets.json')
def surebets():
    try:
        with open('SUREBETS.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404

# Function to start the script in a non-blocking way
def start_script():
    return subprocess.Popen(["./run.sh"], shell=True)

# Function to clean up on exit
def kill_script(process):
    process.kill()

if __name__ == '__main__':
    script_process = start_script()
    atexit.register(kill_script, script_process) # Ensure the script is killed when the Flask app exits
   
    app.run(host='0.0.0.0', port=5000)  # Change host to '0.0.0.0'

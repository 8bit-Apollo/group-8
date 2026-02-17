"""
Counter API Implementation
"""
from flask import Flask, jsonify
from . import status

app = Flask(__name__)

COUNTERS = {}

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return error_response(
            f"Counter {name} already exists",
            status.HTTP_409_CONFLICT
        ) 
    
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    """Delete a counter"""
    if not counter_exists(name):
        return error_response(
            f"Counter {name} does not exist",
            status.HTTP_404_NOT_FOUND
        )
    
    del COUNTERS[name]
    return '', status.HTTP_204_NO_CONTENT

def counter_exists(name):
    """Check if a counter exists"""
    return name in COUNTERS

def error_response(message, code):
    return jsonify({"error": message}), code
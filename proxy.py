#!/usr/bin/env python

import os
import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/firmware/<device>/<buildid>")
def keys(device, buildid):
    filename = f"{device}+{buildid}.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "Data not found"}), 404

if __name__ == "__main__":
    print("running webserver")
    app.run(host='0.0.0.0', port=8888)

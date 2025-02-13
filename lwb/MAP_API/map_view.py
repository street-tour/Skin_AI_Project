from flask import Blueprint, render_template, jsonify
import json
import os
from flask import request, url_for, session

import os
import uuid
from pathlib import Path


map_bp = Blueprint("map", __name__, url_prefix="/map")

@map_bp.route("/kakao/")
def map():
    return render_template("map/kakao.html")

@map_bp.route('/api/hospitals')
def get_hospitals():
    try:
        json_path = os.path.join(os.getcwd(), 'static', 'hospital_data.json')
        
        if not os.path.exists(json_path):
            return jsonify({"error": f"File not found: {json_path}"}), 404

        with open(json_path, encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    map_bp.run(debug=True)
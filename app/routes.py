from flask import Blueprint, request, jsonify

from .models import save_user, get_all_users

routes = Blueprint('routes', __name__)


@routes.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data or 'name' not in data or 'score' not in data:
        return jsonify({"error": "Invalid input"}), 400

    name = data['name']
    score = data['score']

    try:
        result = save_user(name, score)
        return jsonify({
            "message": "Data saved successfully",
            **result
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/results', methods=['GET'])
def results():
    try:
        all_users = get_all_users()
        return jsonify(all_users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

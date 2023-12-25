from flask import Blueprint, request, jsonify
from src.login.verify_login import UserAuthenticator

login_blueprint  = Blueprint('login', __name__)

@login_blueprint.route('/api/login', methods=['POST'])
def login():
    user_login = UserAuthenticator("user_tabel")
    data = request.json
    phonenumber, password = data.get("phonenumber"), data.get("password")
    response, status = user_login.check_login(phonenumber, password)
    return jsonify(response), status
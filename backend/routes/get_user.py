from flask import Blueprint,jsonify,request
from auth_functions.token_in_header_check import token_in_header_check
from database_functions.database_get_user import database_get_user

get_user_endpoint = Blueprint("get_user_endpoint",__name__)

@get_user_endpoint.route("/get_me",methods=["GET"])
def get_user():
    if(request.method == "GET"):
        token = request.cookies.get("Authorization")
        if not token:
            token = request.headers.get("Authorization")
        if token_in_header_check(token=token):
            return database_get_user(token=token)
        else:
            return jsonify({"Error": "Musíte se přihlásit"}),403
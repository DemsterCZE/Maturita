from flask import Blueprint,jsonify,request
from database_functions.database_get_users import database_get_users

get_users_endpoint = Blueprint("get_users",__name__)

@get_users_endpoint.route("/get_users",methods=["GET"])
def get_users():
    if(request.method == "GET"):
        return jsonify({"data":database_get_users()})
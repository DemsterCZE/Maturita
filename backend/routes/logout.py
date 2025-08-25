from flask import make_response,Blueprint,jsonify

logout_endpoint = Blueprint("logout_endpoint",__name__)


@logout_endpoint.route("/logout", methods=["GET"])
def logout():
    response = make_response(jsonify({'Sucess':'Uživate odhlášen'}))
    response.set_cookie("Authorization","",max_age=0)
    return response
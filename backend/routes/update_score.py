from flask import request,Blueprint
from auth_functions.token_in_header_check import token_in_header_check
from database_functions.database_update_score import update_score

update_score_endpoint = Blueprint("update_score_endpoint",__name__)

@update_score_endpoint.route("/update_score",methods=["PATCH"])
def update():
    if request.method == "PATCH":
        token = request.cookies.get("Authorization")
        if not token:
            token = request.headers.get("Authorization")
        data : dict = request.get_json()
        if token_in_header_check(token):
            score = data.get("score")
            if update_score(token=token,score=score):
                return {"Success":"Skóre úspěšně změněno"},200
            else:
                return {"Error":"Něco se pokazilo"}
        else:
            return {"Error": "Nemáš práva"},403
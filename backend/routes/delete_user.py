from flask import redirect,Blueprint,request
from auth_functions.jwt_decode import jwt_decode
from database_functions.delete_user import database_delete_user

delete_user_endpoint = Blueprint("delete_user_endpoint",__name__)

@delete_user_endpoint.route("/delete_user/<id>")
def delete_user(id):
    if request.method == "GET":
        token = request.cookies.get("Authorization")
        try:
            roleID = jwt_decode(token.split(" ",1)[1])['RoleID']
        except:
            return ("Nemáte dostatečná oprávnění"),403
        if roleID == 1:
            database_delete_user(id=id)
            return redirect("/admin_panel")
        else:
            return ("Nemáte dostatečná oprávnění"),403
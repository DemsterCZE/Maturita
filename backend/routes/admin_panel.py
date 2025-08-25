from flask import render_template,Blueprint,request
from database_functions.database_get_users import database_get_users
from auth_functions.jwt_decode import jwt_decode

admin_panel_endpoint = Blueprint("admin_panel_endpoint",__name__,"templates")


@admin_panel_endpoint.route("/admin_panel")
def admin():
    if request.method == "GET":
        users = database_get_users()
        token = request.cookies.get("Authorization")
    try:
        roleID = jwt_decode(token.split(" ",1)[1])['RoleID']
    except:
        return ("Nemáte dostatečná oprávnění"),403
    if roleID == 1:
        return render_template("admin_panel.html",users=users)
    else:
        return ("Nemáte dostatečná oprávnění"),403
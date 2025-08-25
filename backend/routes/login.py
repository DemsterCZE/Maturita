from flask import Blueprint,jsonify,make_response,request
from auth_functions.authentication import authentication

login_endpoint = Blueprint("login_endpoint",__name__)

@login_endpoint.route("/login",methods=["POST"])
def login():
    if request.method == "POST":
        data : dict = request.get_json()
        login = data.get("login")
        password = data.get("password")
         
        if len(login) > 32:
            return jsonify({"Error" : "Uživatelské jméno je moc dlouhé"}),403
        if len(password) > 64:
            return jsonify({"Error" : "Uživatelské heslo je moc dlouhé"}),403
        if(login.isspace() or login == None or login == ""):
            return jsonify({"Error": "Zadejte uživatelské jméno nebo email prosím"}),403
        if(password.isspace() or password == None or login == ""):
            return jsonify({"Error": "Zadejte heslo prosím"}),403
            
        auth = authentication(login=login,password=password)
        if "Error" in auth.keys():
            return jsonify(auth),403
        else:
            response = make_response(jsonify(auth))
            response.set_cookie(key="Authorization",value="Bearer "+auth["Token"],httponly=True,samesite='Strict')
            return response
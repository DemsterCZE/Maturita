from flask import Blueprint,jsonify,request
from database_functions.add_user import add_user
from database_functions.check_for_username_availability import check_for_username_availability
from auth_functions.create_hash import create_hash
from other_functions.validate_email import validate_email


register_endpoint = Blueprint("register_endpoint",__name__)

@register_endpoint.route("/register",methods=["POST"])
def register():
        
    if(request.method == "POST"):
            
        data : dict = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
            
        """Kontrola payloadu"""

        if(password == None or password.isspace() or password == ""):
            return jsonify({"Error": "Zadejte prosím heslo"}),400
        if(username == None or username.isspace() or username == ""):
            return jsonify({"Error": "Zadejte uživatelské jméno prosím"}),400
        if(email == None):
            return jsonify({"Error": "Zadejte email prosím"}),400

        if (len(username)>32):
            return jsonify({"Error": "Zadané jméno je moc dlouhé"}),400
        if(len(email) > 128):
            return jsonify({"Error": "Zadaný email je moc dlouhý"}),400
        if(len(password)) > 64:
            return jsonify({"Error": "Zadané heslo je moc dlouhé"}),400

            
        if(validate_email(email=email)!=True):
            return jsonify({"Error":"Neplatný formát emailu"}),400
        if check_for_username_availability(username=username,email=email) == False:
            return jsonify({"Error": "Uživatelské jméno nebo email je zabrané"}), 400
        hash_function : str = create_hash(password)
        return jsonify(add_user(username=username,
                                    email=email,
                                    password_hash=hash_function))
from flask import Flask,request,jsonify,make_response,send_from_directory,url_for,redirect,render_template
from flask_cors import CORS
import mysql.connector
import argon2 # Hashe
import jwt
import re

"""
Projekt vytvořený pro maturitu

"""

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

key = "Klic"


def update_score(token: str,score : int) -> bool:
    token = token.split(" ",1)[1]
    login = jwt_decode(token=token)["username"]
    database = get_connection()
    
    try:
        cursor = database.cursor()
        cursor.execute("""
        UPDATE users
        SET highest_score=%s
        WHERE username=%s OR email=%s
""",(score,login,login,))
        database.commit()
        cursor.close()
        database.close()
        return True
        
    except mysql.connector.Error as e:
        
        return False
        

def token_in_header_check(token : str) -> bool:
    if token != None:
        token = token.split(" ",1)[1]
        if jwt_decode(token):
            return True
        else:
            return False


def jwt_decode(token:str) -> any:
    try:
        decoded = jwt.decode(token, key, algorithms=["HS256"])
        return decoded
    except:
        return None

def jwt_encode(login : str , roleID : int) -> str:
    encoded = jwt.encode({"username": login,"RoleID": roleID}, key, algorithm="HS256")
    return encoded

def validate_email(email : str) -> bool:
    if re.match(email_regex, email):
        return True 
    else:
        return False

def check_for_username_availability(username : str, email : str) -> bool | dict:
    database = get_connection()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s OR email  = %s", (username,email,))
        result = cursor.fetchone()
        
        if result[0] > 0:
            cursor.close()
            database.close()
            return False  
        else:
            cursor.close()
            database.close()
            return True 

    except mysql.connector.Error as e:
        
        return {"Error" : "Problém s databází"}

"""
Authentication heslo se zkontroluje s uloženým hashem v databázi
"""

def authentication(login : str, password : str) -> dict:
    database = get_connection()
    cursor = database.cursor()
    try:
        cursor.execute(""" SELECT password_hash FROM users WHERE username=%s OR email=%s LIMIT 1""" ,(login,login))
        database_password = cursor.fetchone()
        authenticator = argon2.PasswordHasher()
        if database_password:
            authenticator.verify(hash=database_password[0],password=password)
            cursor.execute('''
            SELECT users.username, roles.RoleID
            FROM users
            INNER JOIN roles ON users.RoleID = roles.RoleID
            WHERE users.username=%s OR users.email=%s
            ''',(login,login))
            data = cursor.fetchone()
            username = data[0]
            role = data[1]
            token = jwt_encode(login=username,roleID=role)
            decoded_token = jwt_decode(token)
            cursor.close()
            database.close()
            return {"Success" : f"Uživatel {decoded_token['username']} úspěšně přihlášen",
            "Token" : token
            }
              
        else:
            cursor.close()
            database.close()
            return {"Error" : "špatné jméno nebo heslo"}

    except argon2.exceptions.VerifyMismatchError as e:
        cursor.close()
        database.close()
        return {"Error" : "špatné jméno nebo heslo"}

def create_hash(passwd : str) -> str:
    hash_builder : argon2.PasswordHasher = argon2.PasswordHasher(salt_len=8,hash_len=24)
    hashed_password : str = hash_builder.hash(passwd)
    return hashed_password

def add_user(username: str, email: str, password_hash: str) -> dict:
    database = get_connection()
    try:
        cursor = database.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, RoleID)
            VALUES (%s, %s, %s, 2)
            """,
            (username, email, password_hash)
        )
        database.commit()
        cursor.close()
        database.close()
        
        return {"Success": "Uživatel registrován"}
    except mysql.connector.Error as e:
        
        return {"Error": "Problém s databází"}

def check_for_table_presence() -> None:
    database = get_connection()
    cursor = database.cursor()
    cursor.execute("SHOW TABLES LIKE 'roles'")
    result2 = cursor.fetchone()
    if result2:
        print("Tabulka roles existuje")
    else:
        cursor.execute('''CREATE TABLE roles(
                       RoleID INT AUTO_INCREMENT PRIMARY KEY,
                       RoleName VARCHAR(20)
                       )
                        ''')
        cursor.execute( '''
                       INSERT INTO roles (RoleName)
                       VALUES ('Admin'),('Player')
                       ''')
        database.commit()


    cursor.execute("SHOW TABLES LIKE 'users'")
    result = cursor.fetchone()
    if result:
        print("tabulka users existuje")
    else:
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(32) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password_hash VARCHAR(128),
                highest_score INT DEFAULT 0,
                RoleID int,
                FOREIGN KEY (RoleID) REFERENCES roles(RoleID)
            )
        """)
        print("Tabulka users vytvořena")

        
        print("Tabulka roles vytvořena")
     
    return
def get_connection():
    return connection_pool.get_connection()

def database_get_users() -> list | dict:
    database = get_connection()
    cursor = database.cursor(dictionary=True)
    try:
        cursor.execute(
        """ SELECT id,username,highest_score FROM users WHERE roleID <> 1 ORDER BY highest_score DESC"""
        )
        users = cursor.fetchall()
    except(mysql.connector.Error):
        cursor.close()
        database.close()
        return {"Error" : "Něco se pokazilo"}
    cursor.close()
    database.close()
    return users

def database_delete_user(id):
    database = get_connection()
    cursor = database.cursor(dictionary=True)
    try:
        cursor.execute(
            """DELETE FROM users WHERE id = %s""",(id,)
        )
    except mysql.connector.Error:
        cursor.close()
        database.close()
        return 
    database.commit()
    cursor.close()
    database.close()
    return 
    


def database_get_user(token:str)-> list | dict:
    database = get_connection()
    cursor = database.cursor(dictionary=True) 
    token = token.split(" ",1)[1]
    decoded_token = jwt_decode(token=token)
    try:
        cursor.execute("""
        SELECT roleID,username,highest_score FROM users WHERE username=%s
        """,(decoded_token['username'],))
        user = cursor.fetchall()
        
    except(mysql.connector.Error):
        cursor.close()
        database.close()
        return {"Error" : "Něco se pokazilo"}
    if user ==[]:
        cursor.close()
        database.close()
        return({"Error":"Uživatel neexistuje"})  
    cursor.close()
    database.close()   
    return user

  
if(__name__ == "__main__"):

    """
    Připojení do databáze
         """
    
    application = Flask(__name__)
    CORS(app=application,origins=["http://127.0.0.1:5000","http://localhost:5000"],supports_credentials=True)
    try: 
        db = {
            "host"  : "xxxxx",
            "user" : "xxxxxx",
            "password" : "xxxxx",
            "database": "xxxxxx"
        }
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **db)
        check_for_table_presence()
        print("Připojení do databáze bylo úspěšné")
    except mysql.connector.Error as E:
        print(E)
    """--------------------------------------------"""
    """Lokální server"""

    @application.route("/get_users",methods=["GET"])
    def get_users():
        if(request.method == "GET"):
           return jsonify({"data":database_get_users()})

    @application.route("/get_me",methods=["GET"])
    def get_user():
        if(request.method == "GET"):
            token = request.cookies.get("Authorization")
            if not token:
                token = request.headers.get("Authorization")
            if token_in_header_check(token=token):
                return database_get_user(token=token)
            else:
                return jsonify({"Error": "Musíte se přihlásit"}),403
            

    @application.route("/logout", methods=["GET"])
    def logout():
        response = make_response(jsonify({'Sucess':'Uživate odhlášen'}))
        response.set_cookie("Authorization","",max_age=0)
        return response

    @application.route("/admin_panel")
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

    @application.route("/register",methods=["POST"])
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

    @application.route("/login",methods=["POST"])
    def login():
        if request.method == "POST":
            data : dict = request.get_json()
            login = data.get("login")
            password = data.get("password")
            
            """
            Kontrola payloadu
                """

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
    
    @application.route("/update_score",methods=["PATCH"])
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
            
    @application.route("/<path:filename>")
    def serve_frontend_files(filename):
        frontend_folder = '../frontend'
        try:
            return send_from_directory(frontend_folder, filename)
        except:
            return ("<p style='font-size: 30px;'>nic</p>"),404
    
    @application.route('/')
    def home():
        return redirect(url_for('serve_frontend_files', filename='index.html'))
    
    
    @application.route("/delete_user/<id>")
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
            

    application.run(debug=True)
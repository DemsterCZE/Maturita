from flask import Flask
from flask_cors import CORS
from routes.admin_panel import admin_panel_endpoint
from routes.delete_user import delete_user_endpoint
from routes.file_server import file_serve_endpoint
from routes.get_user import get_user_endpoint
from routes.get_users import get_users_endpoint
from routes.login import login_endpoint
from routes.logout import logout_endpoint
from routes.register import register_endpoint
from routes.update_score import update_score_endpoint


"""
Projekt vytvořený pro maturitu

"""


  
if(__name__ == "__main__"):

    
    application = Flask(__name__)
    CORS(app=application,origins=["http://127.0.0.1:5000","http://localhost:5000"],supports_credentials=True)
    application.register_blueprint(admin_panel_endpoint)
    application.register_blueprint(delete_user_endpoint)
    application.register_blueprint(file_serve_endpoint)
    application.register_blueprint(get_user_endpoint)
    application.register_blueprint(get_users_endpoint)
    application.register_blueprint(login_endpoint)
    application.register_blueprint(logout_endpoint)
    application.register_blueprint(register_endpoint)
    application.register_blueprint(update_score_endpoint)
    
    
            

    application.run(debug=True)
from flask import send_from_directory,Blueprint,redirect,url_for

file_serve_endpoint = Blueprint("file_serve_endpoint",__name__)

@file_serve_endpoint.route("/<path:filename>")
def serve_frontend_files(filename):
    frontend_folder = '../frontend'
    try:
        return send_from_directory(frontend_folder, filename)
    except:
        return ("<p style='font-size: 30px;'>nic</p>"),404
    
@file_serve_endpoint.route('/')
def home():
    return redirect(url_for('serve_frontend_files', filename='index.html'))
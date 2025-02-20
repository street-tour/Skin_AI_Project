from flask import Blueprint, render_template

main_bp = Blueprint("main",__name__, url_prefix = "/")

@main_bp.route("/")

def index():
    return render_template('index.html') # templates/index.html 을 처리해서 응답
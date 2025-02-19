from flask import Blueprint, render_template
from ..db_utils import main_util

main_bp = Blueprint("main",__name__, url_prefix = "/")

@main_bp.route("/")

def index():
    member_count = main_util.member_count()
    test_count = main_util.test_count()
    wmc = main_util.weekly_member_count() # weekly_member_count
    pc = main_util.product_count() # product_count

    return render_template('index.html',
                            member_count=member_count,
                            test_count=test_count,
                            wmc=wmc) # templates/index.html 을 처리해서 응답
from flask import Blueprint, render_template
from ..db_utils import main_util

main_bp = Blueprint("main",__name__, url_prefix = "/")

@main_bp.route("/")

def index():
    member_count = main_util.member_count()
    test_count = main_util.test_count()
    wmc = main_util.weekly_member_count() # weekly_member_count
    pc = main_util.product_count() # product_count
    wtc = main_util.weekly_test_count() # weekly_test_count

    # product_table 에서 데이터 조회 최근 5개 조회

    product_list = main_util.product_table_list()


    return render_template('index.html',
                            member_count=member_count,
                            test_count=test_count,
                            wmc=wmc,
                            wtc=wtc,
                            pc=pc,
                            product_list=product_list) # templates/index.html 을 처리해서 응답

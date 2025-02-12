from flask import Blueprint, render_template, redirect, request, url_for, send_from_directory
from ..db_utils import board_util, result_util
from flask import session
from ..forms import board_form
from pathlib import Path
import os
import uuid


result_board_bp = Blueprint("result_board", __name__, url_prefix="/result_board")

@result_board_bp.route("/list/")
def list():
    if not session.get('loginuser'):
        return redirect(url_for('auth.login'))
    
    memberid = session['loginuser'].get('memberid')

    import math
    page_no = request.args.get('page_no', 1) # 요청 데이터는 모두 문자열
    pager = {
        "page_no" : int(page_no),  # 현재 페이지 번호
        "page_size" : 3,# 한 페이지에 보여질 글 갯수
        "pager_size": 3, # 한 번에 표시될 페이지 번호
    }
    data_cnt = result_util.select_skin_test_count()
    # pager['page_cnt'] = (data_cnt // pager["page_size"]) + (1 if (data_cnt % pager["page_size"]) >0 else 0 )
    # 데이터 조회(db_utils 사용)
    pager['page_cnt'] = math.ceil(data_cnt / pager['page_size'])
    pager['page_start'] = ( (pager['page_no'] - 1) // pager['pager_size'] ) * pager['pager_size'] + 1
    pager['page_end'] = pager['page_start'] + pager['pager_size']

    start = (pager['page_no'] -1) * pager['page_size']

    skin_test = result_util.select_skin_test_with_paging(memberid=memberid, start=start, page_size=pager["page_size"], result_type='dict')
    return render_template("result_board/result_list.html", pager = pager, skin_test=skin_test)
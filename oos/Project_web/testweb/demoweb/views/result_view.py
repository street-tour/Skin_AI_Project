from flask import Blueprint, render_template, redirect, request, url_for, send_from_directory
from ..db_utils import result_util
from flask import session
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
    
    # skin_test 리스트에서 'tryno' 값만 추출
    tryno_list = [item['tryno'] for item in skin_test if 'tryno' in item]
    # print(tryno_list)  # 추출된 tryno 값 리스트 출력

    model_list = ['eyewrinkles', 'lips', 'chin', 'forehead_1', 'forehead_2', 'cheeks', 'glabella']

    recent_result = {}
    for mo in model_list:
        v = result_util.select_result_by_memberid_and_model(memberid, mo)
        recent_result.update({mo:v})

    # recent_result = result_util.select_result_list_with_tryno(tryno=tryno_list, result_type='dict')
    recent_disease = result_util.select_disease_test(memberid=memberid)
    select_skin_test = result_util.select_skin_test(tryno_list=tryno_list)
    select_skin_test_data = {}
    select_skin_test_data = {}
    if select_skin_test:
        for row in select_skin_test:
            tryno = row[3]  # tryno 값
            model = row[1]  # 모델명 (예: 'forehead_1', 'lips' 등)
            result = row[2]  # 검사 결과 값

            # tryno가 없으면 새 dictionary 생성
            if tryno not in select_skin_test_data:
                select_skin_test_data[tryno] = {}

            # 모델명을 키로 결과값 저장
            select_skin_test_data[tryno][model] = result



    # print(select_skin_test_data)
    # print(recent_disease)
    # print(recent_result)
    return render_template(
        "result_board/result_list.html",
        pager=pager,
        skin_test=skin_test,
        recent_result=recent_result,
        recent_disease=recent_disease,
        select_skin_test=select_skin_test_data  # 수정된 딕셔너리를 전달
    )

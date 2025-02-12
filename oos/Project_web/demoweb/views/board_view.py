from flask import Blueprint, render_template, redirect, request, url_for, send_from_directory
from ..db_utils import board_util
from flask import session
from ..forms import board_form
from pathlib import Path
import os
import uuid


board_bp = Blueprint("board", __name__, url_prefix="/board")

# @board_bp.route("/list/")
# def list():
#     boards= board_util.select_board_list(result_type='dict')
#     return render_template("board/list.html", boards=boards)

@board_bp.route("/list/")
def list():
    import math
    page_no = request.args.get('page_no', 1) # 요청 데이터는 모두 문자열
    pager = {
        "page_no" : int(page_no),  # 현재 페이지 번호
        "page_size" : 3,# 한 페이지에 보여질 글 갯수
        "pager_size": 3, # 한 번에 표시될 페이지 번호
    }
    data_cnt = board_util.select_board_count()
    # pager['page_cnt'] = (data_cnt // pager["page_size"]) + (1 if (data_cnt % pager["page_size"]) >0 else 0 )
    # 데이터 조회(db_utils 사용)
    pager['page_cnt'] = math.ceil(data_cnt / pager['page_size'])
    pager['page_start'] = ( (pager['page_no'] - 1) // pager['pager_size'] ) * pager['pager_size'] + 1
    pager['page_end'] = pager['page_start'] + pager['pager_size']

    start = (pager['page_no'] -1) * pager['page_size']

    boards = board_util.select_board_list_with_paging(start, pager["page_size"], result_type ='dict')
    return render_template("board/list.html", boards = boards, pager = pager)


@board_bp.route('/write/', methods = ["POST","GET"])
def write():
    if not session.get('loginuser'):
        return redirect(url_for('auth.login'))

    form = board_form.BoardForm()

    if request.method.lower() =='post' and form.validate_on_submit():
        # 게시판 테이블에 데이터 저장
        boardno = board_util.insert_board(form.title.data, form.writer.data, form.content.data)

        attachment = request.files.get('attachment')
        if attachment:
            # 파일 저장 (디스크 저장)
            ext = attachment.filename.rsplit('.')[-1]
            unique_file_name = f'{uuid.uuid4().hex}.{ext}' #a/b/c.txt ->['a/b/c/','txt'] -> 'txt'
            bp_path = board_bp.root_path # Blueprint 경로 : views
            root_path = Path(bp_path).parent # 부모 경로 : 여기서는 demoweb
            upload_dir = os.path.join(root_path, "upload-files", unique_file_name)
            attachment.save(upload_dir)

            # 첨부파일 테이블에 데이터 저장
            board_util.insert_attachment(boardno, attachment.filename, unique_file_name)

        return redirect(url_for('board.list'))
    else:
        return render_template('board/write.html', form=form )
    
@board_bp.route("/detail/", methods = ["GET"])
def detail():

    boardno = request.args.get('boardno')
    if not boardno:
        return redirect(url_for('board.list'))
    
    # boardno에 해당하는 게시글 조회수 증가
    read_list = session.get('readlist')
    print("----------------------->", read_list)
    if not read_list:
        read_list=[]
        session['readlist']=read_list
    if boardno not in read_list: # 아직 읽지 않은 글이라면
        board_util.increase_read_count(boardno)
        read_list.append(boardno)
        session['readlist'] = read_list
    
    board = board_util.select_board_by_boardno(boardno, result_type = 'dict')

    attachments = board_util.select_attachments_by_boardno(boardno)
    if not board:
        return redirect(url_for('board.list'))
    else:
        return render_template('board/detail.html', board = board, attachments=attachments)
    
@board_bp.route('/delete/', methods=['GET'])
def delete():
    boardno = request.args.get('boardno');
    if boardno:
        board_util.delete_board(boardno)
    return redirect(url_for('board.lst'))

@board_bp.route('/update/', methods=['GET','POST'])
def update():
    if request.method.lower() == 'get':
        boardno = request.args.get('boardno')
        if not boardno:
            return redirect(url_for('board.list'))
        
        board = board_util.select_board_by_boardno(boardno, result_type='dict')
        if not board:
            return redirect(url_for('board.list'))
        else:
            return render_template('board/update.html', board=board)
        
    else:
        boardno = request.form.get('boardno')
        title = request.form.get('title')
        content = request.form.get('content')
        board_util.update_board(boardno, title, content)

        return redirect(url_for('board.detail', boardno = boardno))
    
@board_bp.route("/download/", methods=["GET"])
def download():
    savedfilename = request.args.get('savedfilename')
    bp_path = board_bp.root_path # Blueprint 경로 : views
    root_path = Path(bp_path).parent # 부모 경로 : 여기서는 demoweb
    upload_dir = os.path.join(root_path, "upload-files")

    return send_from_directory(upload_dir, savedfilename, as_attachment=True)
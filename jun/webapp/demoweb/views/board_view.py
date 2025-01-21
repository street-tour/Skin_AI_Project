from flask import Blueprint, render_template, redirect, request, url_for
from ..db_utils import board_util
from flask import session
from ..forms import board_form


board_bp = Blueprint("board", __name__, url_prefix="/board")

@board_bp.route("/list/")
def list():
    boards= board_util.select_board_list(result_type='dict')
    return render_template("board/list.html", boards=boards)

@board_bp.route('/write/', methods = ["POST","GET"])
def write():
    if not session.get('loginuser'):
        return redirect(url_for('auth.login'))

    form = board_form.BoardForm()

    if request.method.lower() =='post' and form.validate_on_submit():
        
        board_util.insert_board(form.title.data, form.writer.data, form.content.data)
        return redirect(url_for('board.list'))
    else:
        return render_template('board/write.html', form = form)
    
@board_bp.route("/detail/", methods = ["GET"])
def detail():

    boardno = request.args.get('boardno')
    if not boardno:
        return redirect(url_for('board.list'))
    
    board = board_util.select_board_by_boardno(boardno, result_type = 'dict')

    return render_template('board/detail.html', board = board)
    
    

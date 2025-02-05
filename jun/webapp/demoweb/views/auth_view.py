from flask import Blueprint
from flask import render_template  # forward 방식 이동
from flask import request #요청 관련 정보를 저장하는 객체
from flask import redirect # redirect 방식 이동
from flask import url_for, session
from werkzeug.security import generate_password_hash # 복원불가능암호화 도구
from werkzeug.security import check_password_hash # 암호화 데이터 비교


from ..forms import auth_form
from ..db_utils import auth_util



auth_bp = Blueprint("auth", __name__, url_prefix = "/auth")

@auth_bp.route("/sign-up/", methods = ["GET","POST"])
def register():
    form = auth_form.RegisterForm()
    if request.method.lower() == 'post'and form.validate_on_submit():

        print(form.gender.data, request.form.get('gender'))
        print(form.skin.data, request.form.get('skin'))
        return 'test'
    
        passwd_hash = generate_password_hash(form.passwd.data)
        auth_util.insert_member(form.memberid.data, passwd_hash, form.email.data)
        return redirect( url_for('auth.login'))
    else:
       return render_template("auth/sign-up.html", form = form)
    

@auth_bp.route("/login/", methods = ["GET","POST"])
def login():
    form = auth_form.LoginForm()
    if request.method.lower() == 'post'and form.validate_on_submit():
    
        # 1. memberid 로 데이터베이스에서 데이터 조회
        member = auth_util.select_member_by_id(form.memberid.data)
        # 2 -1. 조회된 데이터가 없으면 로그인 실패
        if not member:
            return render_template('auth/login.html',
                                    error='해당 아이디의 사용자가 없습니다.', form = form) # html로 데이터를 전달

        # 2 -2. 조회된 데이터가 있으면 패스워드 비교
        if not check_password_hash(member[1], form.passwd.data):  # 3. 패스워드가 다르면 로그인 실패
            return render_template('auth/login.html',
                                    error = "패스워드가 일치하지 않습니다.", form=form) # html로 데이터를 전달
        
        else:   # 4. 패스워드가 같으면 로그인 처리 -> 세션에 데이터 저장
            session['loginuser'] = { k: v for k,v in zip(['memberid','passwd','email'], member) if k != 'passwd'}
            return redirect(url_for("main.index")) 
    else:
       return render_template("auth/login.html", form = form)

        
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear() #세션의 모든 요소를 제거

    return redirect(url_for('main.index'))
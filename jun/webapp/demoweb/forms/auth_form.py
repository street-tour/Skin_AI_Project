# pip install flask-wtf # flask Form을 사용하기 위해 설치
# pip install email-validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Email



class LoginForm(FlaskForm):
    memberid = StringField("아이디", validators = [DataRequired("아이디를 입력하세요")])
    passwd = PasswordField("패스워드", validators = [DataRequired("패스워드를 입력하세요")])
    
class RegisterForm(LoginForm):
    memberid = StringField("아이디", validators = [DataRequired("아이디를 입력하세요")])
    passwd = PasswordField("패스워드", validators = [DataRequired("패스워드를 입력하세요")])
    email = EmailField("이메일", validators = [Email("이메일 형식이 적합하지 않습니다")])
    gender = RadioField('성별',
                        choices = [('male','남'), ('female','여')], validators = [DataRequired("성별을 선택하세요")])
    skin = RadioField('피부 타입',
                      choices = [('dry','건성'),('oily','지성'),('combination','복합성')], validators =[DataRequired('피부 타입을 선택하세요')])
    
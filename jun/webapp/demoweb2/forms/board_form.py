from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField
from wtforms.validators import DataRequired

class BoardForm(FlaskForm):
    title = StringField('제목', validators = [DataRequired("제목을 입력하세요")])
    writer = StringField('제목', validators = [DataRequired("로그인 하세요")])
    content = StringField('제목', validators = [DataRequired("내용을 입력하세요")])
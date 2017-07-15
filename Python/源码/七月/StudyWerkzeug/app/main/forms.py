from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class loginForm(Form):
    username = StringField('用户名',validators=[DataRequired()])
    password = StringField('用户密码',validators=[DataRequired()])
    submit = SubmitField('提交')

class registForm(Form):
    email = StringField('邮箱',validators=[DataRequired()])
    username = StringField('用户名',validators=[DataRequired()])
    password = StringField('用户密码',validators=[DataRequired()])
    submit = SubmitField('提交')
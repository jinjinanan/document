from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('Email',validators=[DataRequired(),Length(1,50),Email()])
    password = StringField('Password',validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    email = StringField('Email',validators=[DataRequired(),Length(1,50),Email()])
    #正则表达式，旗标，消息提示
    username = StringField('Username',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                                                   flags=0,
                                                                                   message='Usernames must have only letters, '
                                                                                   'numbers, dots or underscores')
                           ])
    # 这个验证函数要附属到两个密码字段中 的一个上，另一个字段则作为参数传入
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField('Register')

    # 如果表单类中定义了以validate_开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Eamil already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('UserName already registered.')


class ModifyPassword(Form):
    odlPassword = PasswordField('Old Password',validators=[DataRequired()])
    newPassword1 = PasswordField('New Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class ResetPassword(Form):
    userName = StringField('UserName',validators=[DataRequired(),Length(1,64)])
    submit = SubmitField('Submit')

class ModifyEmail(Form):
    email = StringField('Email',validators=[DataRequired(),Email(),Length(1,50)])
    sumbit = SubmitField('Submit')




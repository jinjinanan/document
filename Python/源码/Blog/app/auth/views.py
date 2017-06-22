from flask import render_template,redirect,request,url_for,flash,g
from . import auth
from flask_login import login_required,login_user,logout_user,current_user
from ..models import User
from .forms import LoginForm,RegistrationForm,ModifyPassword,ModifyEmail,ResetPassword,ValidEmail
from .. import db
from ..email import send_mail

#如果 before_request 或 before_app_request 的回调返回响应或重定
@auth.before_app_request
def before_request():
    # 用户已登录
    # 用户未认证
    # 请求的端点(使用 request.endpoint 获取)不在认证蓝本中。访问认证路由要获取权
    # 限，因为这些路由的作用是让用户确认账户或执行其他账户管理操作。
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':        #切片 截取前5个字符
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')      # get_flashed_messages 开放给模版
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required     # Flask-Login 提供login_required 保护路由只让认证用户访问
def logout():
    logout_user()                           #删除并重设用户会话
    flash('You have been logged out.')      #显示一个 Flash 消息
    return redirect(url_for('main.index'))  #重定向到首页

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data,
                    role_id = 0)
        db.session.add(user)
        # 程序已经可以在请求末尾自动提交数据库变化，这里也要添加 db.session.commit() 调用。问题在于，提交数据库之后才能赋予新用户
        # id 值，而确认令牌需要用到 id，所以不能延后提交。
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email,'Confirm Your Account','auth/email/confirm',user=user,token=token)
        flash('A confirmation email has been send your by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html',form = form)

@auth.route('/confirm/<token>')
@login_required #Flask-Login 提供的 login_required 修饰器会保护这个路由，因此，用户点击确认邮件中的
                #链接后，要先登录，然后才能执行这个视图函数。
def confirm(token):
    # 如果确认过，则重定向到首页
    # import pdb; pdb.set_trace()
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    # User 模型中 confirmed 属性的值会 被修改并添加到会话中，请求处理完后，这两个操作被提交到数据库
    if current_user.confirm(token):
        flash('You have confirmed your account,Thanks!')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email,'Confirm Your Account','auth/email/confirm',user = current_user,token = token)
    flash('A new confirmation email has been sent to you')
    return redirect(url_for('main.index'))


#安全设置
@auth.route('/SecuritySetting')
@login_required
def SecuritySetting():
    return render_template('auth/SecuritySetting/SecuritySetting.html')


# 修改电子邮件
@auth.route('/ModifyPassword' ,methods = ['GET','POST'])
@login_required
def ModifyPassWord():
    form = ModifyPassword()
    if form.validate_on_submit():
        oldPadssword = form.odlPassword.data
        if current_user.verify_password(oldPadssword):
            current_user.password = form.newPassword1.data
            db.session.add(current_user)
            db.session.commit()
            flash('Modify password success!')
            return redirect(url_for('main.index'))
        else:
            return render_template(url_for('auth.SecuritySetting'))
    return render_template('auth/SecuritySetting/ModifyPassword.html',form = form)

#修改密码
@auth.route('/ModifyEmail', methods = ['GET','POST'])
@login_required
def Modifyemail():
    form = ModifyEmail()
    if form.validate_on_submit():
        current_user.reset_email = form.email.data
        token = current_user.generate_confirmation_token()
        send_mail(current_user.reset_email,'Confirm Your Account','auth/email/changeEmail',user = current_user,token = token)
        flash('A confirmation email has been send your by email.')
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('auth/SecuritySetting/ModifyEmail.html',form = form)


@auth.route('/confirmNewEmail/<token>')
@login_required
def confimNewEmail(token):
    if current_user.confirm(token):
        current_user.email = current_user.reset_email
        current_user.reset_email = ''
        db.session.add(current_user)
        db.session.commit()
        flash('修改邮箱成功')
        return redirect(url_for('main.index'))
    else:
        flash('修改邮箱失败')
        return redirect(url_for('auth.SecuritySetting'))

#忘记密码
@auth.route('/ForgetPassword',methods = ['GET','POST'])
def forgetPassword():
    form = ValidEmail()
    if form.validate_on_submit():
        newEmail = form.email.data
        user = db.session.query(User).filter(User.email == newEmail).first()
        if user is not None:
            flash('a email has been send your mailbox')
            send_mail(form.email.data, 'Found Your Account',
                      'auth/email/resetPassword',token =user.generate_confirmation_token )
            redirect(url_for('main.index'))
        else:
            flash('not have user')
    return render_template('auth/SecuritySetting/ValidEmail.html',form = form)

#忘记密码正在建设中
@auth.route('/confirmUser-ForgetPassword/<token>',methods = ['GET','POST'])
def confirmUser_ForgetPassword(token):
    form = ResetPassword()
    if form.validate_on_submit():
        pass
    return render_template('auth/SecuritySetting/ResetPassword.html',form = form)

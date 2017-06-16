from threading import Thread
from flask import current_app,render_template
from flask_mail import Message
from . import mail

def send_mail(to,subject,template, **kwargs):
    app = current_app._get_current_object()
    # 为收件人地址、主题、渲染邮件正文的模板和关键字参数列表

    #  指定模板时不能包含扩展名，这样才能使用两个模板分别渲染纯文本正文和富文本正文
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+ '' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)  #通过可变字符串，穿参数
    msg.html = render_template(template+'.html',**kwargs)
    mail.send(msg)
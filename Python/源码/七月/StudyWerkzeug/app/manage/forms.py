from flask_wtf import Form
from wtforms import SubmitField
from flask_wtf.file import FileField,FileRequired,FileAllowed

ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

class uploadForm(Form):
    file = FileField(u'文件上传',
                     validators = [FileAllowed(ALLOWED_EXTENSIONS,u'不合法'),FileRequired(u'文件未选择')])
    submit = SubmitField('提交')

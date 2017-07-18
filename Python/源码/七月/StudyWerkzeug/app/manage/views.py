from . import manage
import os
from flask_login import login_required
from .forms import uploadForm
from flask import request,redirect,url_for,render_template,flash
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])


def allowed_file(filename):
    return '.' in filename and filename.resplit('.',1)[1] in ALLOWED_EXTENSIONS

@manage.route('/manage/upload',methods = ['GET','POST'])
def upload():
    form = uploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        import pdb
        pdb.set_trace()
        form.file.data.save(os.path.join('/Users/chenlinbo/Desktop/test',filename))
        flash('成功')
    else:
        filename = None
        flash('不成功')
    return render_template('upload_file.html',form = form)


@manage.route('/manage')
@login_required
def manage():
    return render_template('manage.html')

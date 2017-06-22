#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template,abort,flash,redirect,url_for
from . import main
from ..models import User
from .. import db
from flask_login import login_required,current_user
from ..decorators import admin_required, permission_required
from ..models import Permission
from .forms import EditProfileForm

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

#查看用户详情
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user = user)

#编辑用户资料
@main.route('/edit-profile',methods = ['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user',username = current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('EditProfile.html',form = form)







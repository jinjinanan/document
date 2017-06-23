#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template,abort,flash,redirect,url_for,request
from . import main
from ..models import User,Post
from .. import db
from flask_login import login_required,current_user
from ..decorators import admin_required, permission_required
from ..models import Permission
from .forms import EditProfileForm,PostForm

@main.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        # current_user 这个对象的表现类似用户对象，但实际上却是一个轻度包装，包含真正的用户对象。
        # 数据库需要真正的用户对象，因此要调用 _get_current_object() 方法
        post = Post(body = form.body.data,author = current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    # page = request.args.get('page', 1, type=int)
    # # #页 数是 paginate() 方法的第一个参数，也是唯一必需的参数
    # # #可选参数 per_page 用来指定 每页显示的记录数量;如果没有指定，则默认显示 20 个记录
    # # #error_ out，当其设为 True 时(默认值)，如果请求的页数超出了范围，则会返回 404 错误;如果 设为 False，页数超出范围时会返回一个空列表
    # pagination = Post.query.order_by(Post.timestamp.desc())\
    #     .paginate(page,per_page=20,
    #               error_out=False)
    # posts = pagination.items
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',form = form)


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
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user = user,posts = posts)

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











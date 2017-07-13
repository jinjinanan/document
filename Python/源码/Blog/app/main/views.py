#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template,abort,flash,redirect,url_for,request,make_response
from . import main
from ..models import User,Post,Comment
from .. import db
from flask_login import login_required,current_user
from ..decorators import admin_required, permission_required
from ..models import Permission
from .forms import EditProfileForm,PostForm,CommentForm

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        # current_user 这个对象的表现类似用户对象，但实际上却是一个轻度包装，包含真正的用户对象。
        # 数据库需要真正的用户对象，因此要调用 _get_current_object() 方法
        post = Post(body = form.body.data,author = current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))

    show_followed = False
    # import pdb
    # pdb.set_trace()
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))

    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query


    page = request.args.get('page', 1, type=int)
    # #页 数是 paginate() 方法的第一个参数，也是唯一必需的参数
    # #可选参数 per_page 用来指定 每页显示的记录数量;如果没有指定，则默认显示 20 个记录
    # #error_ out，当其设为 True 时(默认值)，如果请求的页数超出了范围，则会返回 404 错误;如果 设为 False，页数超出范围时会返回一个空列表
    pagination = query.order_by(Post.timestamp.desc())\
        .paginate(page,per_page=20,
                  error_out=False)
    posts = pagination.items
    # import pdb
    # pdb.set_trace()
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',form = form,
                           posts = posts,pagination = pagination)


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

#每篇文章都要有一个专页，使用唯一的 URL 引用
@main.route('/post/<int:id>',methods = ['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body = form.body.data,post=post,
                          author = current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post',id=post.id,page = -1))
    page = request.args.get('page',1,type=int)
    if page == -1:
        page = (post.comments.count() - 1) // 20 +1
    pagination = post.comments.order_by(Comment.timestamp.asc())\
        .paginate(page,per_page=20,error_out=False)
    comments = pagination.items
    return  render_template(
        'post.html',posts = [post],form = form,
        comments = comments,pagination = pagination
    )

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    import pdb
    pdb.set_trace()
    if current_user != post.author and not current_user.can(Permission.ADMINTSTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated')
        return redirect(url_for('.post',id = post.id))
    form.body.data = post.body
    return render_template('edit_post.html',form = form)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user',username = username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user',username = username))

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type = int)
    pagination = user.followers.paginate(
        page,per_page=20,error_out=False
    )
    follows = [{'user':item.follower,'timestamp':item.timestamp}
               for item in pagination.items]
    return render_template('followers.html',user = user,title = 'Followers of',
                           endpoint = '.followers', pagination = pagination,
                           follows = follows)



@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type = int)
    pagination = user.followed.paginate(
        page,per_page=20,error_out=False
    )
    follows = [{'user':item.followed,'timestamp':item.timestamp}
                for item in pagination.items]
    # import pdb
    # pdb.set_trace()
    return render_template('followers.html',user = user,title = 'Followed by',
                           endpoint = '.followed_by',pagination = pagination,
                           follows = follows)

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username = username).first()
    import pdb
    pdb.set_trace()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are already unfollow this user.')
        return redirect(url_for('.index'))
    current_user.unfollow(user)

    flash('You are not following %s'% username)
    return  redirect(url_for('.user',username = username))


@main.route('/all')
@login_required
def show_all():
    # import pdb
    # pdb.set_trace()
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','',max_age = 30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    # import pdb
    # pdb.set_trace()
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1',max_age = 30*24*60*60)
    return resp





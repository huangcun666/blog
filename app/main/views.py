from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response,g
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
    CommentForm,SearchForm,Refresh
from .. import db
from ..models import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required
from datetime import datetime
import random,os,flask_whooshalchemyplus,re

@main.before_app_request
def before_request():
    g.search_form = SearchForm()

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'

@main.route('/writepost', methods=['GET', 'POST'])
@login_required
def writepost():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        rep = re.compile('>(.*?)<')
        string1 = ''
        for str in rep.findall(form.body.data):
            string1 += str
        rep1 = re.compile('><')
        string1 = rep1.sub('', string1)
        rep2 = re.compile('\s')
        string1 = rep2.sub('', string1)
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object(),
                    body_count=len(string1),
                    love=0)
        current_user.body_counts+=len(string1)
        db.session.add(post)
        db.session.add(current_user)
        return redirect(url_for('.index'))
    return render_template('writepost.html',form=form)

def gen_rnd_filename():
    filename_prefix = datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (current_user.username+filename_prefix, str(random.randrange(1000,10000)))

@main.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(main.static_folder, 'upload', rnd_name)

        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response

@main.route('/', methods=['GET', 'POST'])
def index():
    form=Refresh()
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    users=User.query.filter(User.body_counts>1000).all()
    users1=[]
    loves_body_count={}
    for user in users:
        num=0
        for post in user.posts:
            num+=post.love
        if num>=1:
            if current_user.is_anonymous:
                users1.append(user)
                loves_body_count[user]=[(round(user.body_counts/1000,2)),num]
            elif not current_user.is_following(user):
                users1.append(user)
                loves_body_count[user] = [(round(user.body_counts / 1000, 2)), num]
    random.shuffle(users1)
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('index.html',  posts=posts,users=users1,
                           loves_body_count=loves_body_count,form=form,
                           show_followed=show_followed, pagination=pagination)

@main.route('/search',methods=['GET', 'POST'])
def search():
    flask_whooshalchemyplus.index_all(current_app)
    if g.search_form.validate_on_submit():
        query=g.search_form.search.data
        results = Post.query.whoosh_search(query).all()
        g.search_form.search.data = query
        return render_template('search.html',
                               query=query,
                               results=results)
    else:
        return redirect(url_for('.index'))


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    loves=0
    for post in user.posts:
        loves+=post.love
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,loves=loves,
                           pagination=pagination)

@main.route('/love/<int:id>',methods=['GET','POST'])
@login_required
def love(id):
    post=Post.query.get_or_404(id)
    current_user.userloves.append(post)
    post.love+=1
    db.session.add(post)
    db.session.add(current_user)
    return redirect(url_for('.post',id=id))

@main.route('/notlove/<int:id>',methods=['GET','POST'])
@login_required
def notlove(id):
    post=Post.query.get_or_404(id)
    current_user.userloves.remove(post)
    post.love-=1
    db.session.add(post)
    db.session.add(current_user)
    return redirect(url_for('.post',id=id))

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data

        avatar=request.files['avatar']
        if avatar:
            fname=avatar.filename
            UPLOAD_FOLDER=current_app.config['UPLOAD_FOLDER']
            ALLOWED_EXTENSIONS=['png','jpg','jpeg','gif','bmp']
            flag='.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
            if not flag:
                flash('文件类型错误')
                return redirect(url_for('.user',username=current_user.username))
            avatar.save('{}{}_{}'.format(UPLOAD_FOLDER,current_user.username,fname))
            current_user.real_avatar="/static/avatar/{}_{}".format(current_user.username,fname)
        db.session.add(current_user)
        flash('你的资料已经更新.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data

        avatar = request.files['avatar']
        if avatar:
            fname = avatar.filename
            UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
            ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
            flag = '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
            if not flag:
                flash('文件类型错误')
                return redirect(url_for('.user', username=user.username))
            avatar.save('{}{}_{}'.format(UPLOAD_FOLDER,user.username, fname))
            user.real_avatar = "/static/avatar/{}_{}".format(user.username, fname)
        db.session.add(user)
        flash('你的资料已经更新.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile_admin.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    user = User.query.get_or_404(post.author_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('你发表了评论')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,user=user,id=id,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.title=form.title.data
        db.session.add(post)
        flash('博客已经更新')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.title.data=post.title
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在的用户')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    return redirect(url_for('.user', username=username))

@main.route('/user_follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def user_follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在的用户')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        return redirect(url_for('.index'))
    current_user.follow(user)
    return redirect(url_for('.index'))

@main.route('/yfollow/<username>/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def yfollow(username,id):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在的用户')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        return redirect(url_for('.post', id=id))
    current_user.follow(user)
    return redirect(url_for('.post', id=id))

@main.route('/yunfollow/<username>/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def yunfollow(username,id):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在的用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        return redirect(url_for('.post', id=id))
    current_user.unfollow(user)
    return redirect(url_for('.post', id=id))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在的用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    return redirect(url_for('.user', username=username))

@main.route('/user_unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def user_unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在的用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        return redirect(url_for('.index', username=username))
    current_user.unfollow(user)
    return redirect(url_for('.index', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="的粉丝",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="的关注",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))

@main.route('/rel_delete_post/<int:id>')
@login_required
def rel_delete_post(id):
    post=Post.query.get_or_404(id)
    return render_template('deletepost.html',post=post)

@main.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    post=Post.query.get_or_404(id)
    rep = re.compile('>(.*?)<')
    string1 = ''
    for str in rep.findall(post.body_html):
        string1 += str
    rep1 = re.compile('><')
    string1 = rep1.sub('', string1)
    rep2 = re.compile('\s')
    string1 = rep2.sub('', string1)
    current_user.body_counts-=len(string1)
    db.session.delete(post)
    db.session.add(current_user)
    flash('你删除了一条博客')
    return redirect(url_for('.index'))

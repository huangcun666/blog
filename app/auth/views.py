from flask import render_template, redirect, request, url_for, flash,session
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm,ChangeUsername

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            session.permanent=True
            login_user(user,remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        user1=User.query.filter_by(username=form.email.data).first()
        if user1 is not None and user1.verify_password(form.password.data):
            login_user(user1,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户或密码密码错误')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hasuser=User.query.filter_by(email=form.email.data).first()
        hasuser1=User.query.filter_by(username=form.username.data).first()
        if hasuser:
            return render_template('auth/register.html',form=form,hasemail=hasuser.email)
        elif hasuser1:
            return render_template('auth/register.html', form=form, haseuser=hasuser1.username)
        else:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        body_counts=1,
                        name='')
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email,'验证你的账号',
                       'auth/email/confirm', user=user, token=token)
            flash('验证邮件已经发送到你的电子邮箱')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经验证了你的账号')
    else:
        flash('确认链接无效或者已经过期')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'验证你的账号',
               'auth/email/confirm', user=current_user, token=token)
    flash('一封新的验证邮件已经发送到你的邮箱')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('更改密码成功')
            return redirect(url_for('main.index'))
        else:
            flash('无效的密码')
            return redirect(url_for('auth.change_password'))
    return render_template("auth/change_password.html", form=form)

@auth.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsername()
    if form.validate_on_submit():
            current_user.username= form.username.data
            db.session.add(current_user)
            flash('更改用户名成功')
            return redirect(url_for('main.index'))
    return render_template("auth/change_username.html", form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '更改密码',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
            flash('更改密码的邮件已经发送到你的邮箱')
        flash('邮箱没有注册')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('更改密码成功')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '验证你的邮箱地址',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('验证你新邮箱地址的邮件已经发送到你的新邮箱')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('你的邮箱地址修改成功')
    else:
        flash('无效的请求')
    return redirect(url_for('main.index'))

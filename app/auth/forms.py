from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱:', validators=[Required(), Length(1, 64)])
    password = PasswordField('密码:', validators=[Required()])
    remember_me = BooleanField('记住我',default=True)
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1,8)])
    password = PasswordField('Password', validators=[
        Required(),Length(6,12), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('注册')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[Length(6,12),
        Required(), EqualTo('password2', message='密码必须匹配')])
    password2 = PasswordField('验证你的密码', validators=[Required(),Length(6,12)])
    submit = SubmitField('更改密码')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重设密码')

class ChangeUsername(FlaskForm):
    username = StringField('新的用户名', validators=[Required(), Length(1,8)])
    submit = SubmitField('修改用户名')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError('用户名已经注册过了')

class PasswordResetForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[Length(6,12),
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('验证密码', validators=[Required()])
    submit = SubmitField('重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('没有注册的邮箱地址')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[Required(), Length(1, 64),Email()])
    password = PasswordField('密码', validators=[Required(),Length(6,12)])
    submit = SubmitField('更改邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册过了')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,FileField,TextField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User

class Refresh(FlaskForm):
    submit=SubmitField('刷新')

class NameForm(FlaskForm):
    name = StringField('你的名字?', validators=[Required()])
    submit = SubmitField('提交')

class SearchForm(FlaskForm):
    search=TextField('search',validators=[Required()])

class EditProfileForm(FlaskForm):
    name = StringField('个性标签', validators=[Length(0,5)])
    location = StringField('来自', validators=[Length(0, 64)])
    about_me = TextAreaField('个人介绍')
    avatar=FileField('头像')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1,8)])
    confirmed = BooleanField('验证')
    role = SelectField('角色', coerce=int)
    name = StringField('个性标签', validators=[Length(0,5)])
    location = StringField('来自', validators=[Length(0, 64)])
    about_me = TextAreaField('个人介绍')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    title=StringField('标题',validators=[Required()])
    body = TextAreaField("正文", validators=[Required()])
    submit = SubmitField('提交')

class CommentForm(FlaskForm):
    body = TextAreaField('评论', validators=[Required()])
    submit = SubmitField('提交')

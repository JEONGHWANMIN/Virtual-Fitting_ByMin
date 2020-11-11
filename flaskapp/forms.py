from flask_wtf import FlaskForm
from models import Users
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('re_password')]) #equalTo("필드네임")
    re_password = PasswordField('re_password', validators=[DataRequired()])
    birthday_year = StringField('birthday_year', validators=[DataRequired()])
    # birthday_month = SelectField('birthday_month', choices=[('january','1'), ('february','2'), ('march','3'), ('april','4'), ('may','5'), ('june','6'), ('july','7'), ('august','8'), ('september','9'), ('october','10'), ('november','11'), ('december','12')])
    birthday_month = StringField('birthday_month', validators=[DataRequired()])
    birthday_day = StringField('birthday_day', validators=[DataRequired()])
    sex = SelectField('sex', choices=[('man', '남성'), ('women', '여성')])
    phone = StringField('phone', validators=[DataRequired()])

class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
        def __call__(self,form,field):
            userid = form['userid'].data
            password = field.data
            users = Users.query.filter_by(userid=userid).first()
            if users == None:
                raise ValueError('존재하지 않는 사용자입니다.')
            elif users.password != password:
                # raise ValidationError(message % d)
                raise ValueError('비밀번호가 일치하지 않습니다.')
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])

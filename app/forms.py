from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, IPAddress, Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, DeviceType


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    #openid = StringField('openid',validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[
                                    DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('user is exists,input other username.')


class SingleForm(FlaskForm):
    ipaddress = StringField('IP address',
                            validators=[DataRequired(), IPAddress()])
    device_model = SelectField('设备型号', validators=[Required()], coerce=str)
    login_type = SelectField('登陆方式',
                             validators=[Required('Select login type')],
                             choices=[('telnet', 'Telnet'), ('ssh', 'SSH')],
                             coerce=str)
    username = StringField('Username')
    password = PasswordField('Password')
    enable_password = PasswordField(
        'Enalbe Password', validators=[DataRequired()])
    submit = SubmitField('普通巡检')
    submit2 = SubmitField('深度巡检')

    def __init__(self, *args, **kwargs):
        super(SingleForm, self).__init__(*args, **kwargs)
        self.device_model.choices = [(device.device_model, device.device_model)
                                     for device in DeviceType.query.order_by(DeviceType.id).all()]
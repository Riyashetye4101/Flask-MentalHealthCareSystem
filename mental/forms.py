from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length, Email,DataRequired,ValidationError
from mental.models import Customer
class Registeration(FlaskForm):
    def validate_username(self,username_to_check):
        user=Customer.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Account already exist with this username , please create the account with different username')
    def validate_email_address(self,email_address_to_check):
        email=Customer.query.filter_by(email=email_address_to_check.data).first()
        if email:
            raise ValidationError('Account already exist with this email address, please create the account with different email')

    def validate_mobile(self,mobile_to_check):
        no=Customer.query.filter_by(mobile=mobile_to_check.data).first()
        if no:
            raise ValidationError('Account already exist with this mobile no, please create the account with different mobile no')

    username=StringField(label='username',validators=[length(min=2,max=13),DataRequired()])
    name=StringField(label='name',validators=[length(min=2,max=100),DataRequired()])
    email_address=StringField(label='email',validators=[Email(),DataRequired()])
    password=PasswordField(label='password',validators=[length(min=8,max=13),DataRequired()])
    mobile=StringField(validators=[length(min=10,max=10),DataRequired()])
    age=StringField(validators=[length(min=1,max=3),DataRequired()])
    submit=SubmitField(label='Sign Up')

class Login(FlaskForm):
    username=StringField(label='Username',validators=[DataRequired()])
    password=PasswordField(label='password',validators=[DataRequired()])
    submit=SubmitField(label='Sign In')

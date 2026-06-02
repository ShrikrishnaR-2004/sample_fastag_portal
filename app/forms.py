# pyrefly: ignore [missing-import]
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, DateField, SelectField,
    BooleanField, HiddenField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, Optional,
    Regexp, ValidationError
)
import re
def strong_password(form, field):
    pw = field.data or ''
    errors = []
    if len(pw) < 8:
        errors.append('at least 8 characters')
    if not re.search(r'[A-Z]', pw):
        errors.append('one uppercase letter')
    if not re.search(r'[0-9]', pw):
        errors.append('one number')
    if not re.search(r'[!@#$%^&*]', pw):
        errors.append('one special character (!@#$%^&*)')
    if errors:
        raise ValidationError('Password must contain: ' + ', '.join(errors) + '.')
def indian_mobile(form, field):
    num = (field.data or '').replace(' ', '').strip()
    if not re.fullmatch(r'\d{10}', num):
        raise ValidationError('Enter a valid 10-digit mobile number.')
def valid_aadhaar(form, field):
    raw = (field.data or '').replace(' ', '').replace('•', '')
    if raw and not re.fullmatch(r'\d{12}', raw):
        raise ValidationError('Aadhaar must be exactly 12 digits.')
def valid_pan(form, field):
    if field.data and not re.fullmatch(r'[A-Z]{5}[0-9]{4}[A-Z]', field.data.upper()):
        raise ValidationError('Enter a valid 10-character PAN (e.g. ABCDE1234F).')
def valid_vehicle_reg(form, field):
    vrn = (field.data or '').upper().replace(' ', '')
    if vrn and not re.fullmatch(r'[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{4}', vrn):
        raise ValidationError('Enter a valid vehicle registration number (e.g. TN01AB1234).')
class LoginForm(FlaskForm):
    mobile   = StringField('Mobile Number',
                           validators=[DataRequired(message='Mobile number is required.'),
                                       indian_mobile])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Password is required.')])
    captcha  = StringField('Captcha',
                           validators=[DataRequired(message='Captcha is required.')])
    submit   = SubmitField('Sign In')
class SignupForm(FlaskForm):
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=2, max=120)])
    phone     = StringField('Phone Number',
                            validators=[DataRequired(), indian_mobile])
    email     = StringField('Email Address',
                            validators=[DataRequired(), Email(message='Enter a valid email.')])
    dob       = DateField('Date of Birth',
                          validators=[DataRequired(message='Date of birth is required.')])
    aadhaar     = HiddenField('Aadhaar (raw digits)')   
    aadhaar_display = StringField('Aadhaar Number',
                                  validators=[Optional(), valid_aadhaar])
    pan         = StringField('PAN Number',
                              validators=[Optional(), valid_pan])
    vehicle_reg  = StringField('Vehicle Registration Number',
                               validators=[Optional(), valid_vehicle_reg])
    vehicle_type = SelectField('Vehicle Type',
                               choices=[
                                   ('', '— Select vehicle type —'),
                                   ('two-wheeler', 'Two Wheeler'),
                                   ('four-wheeler', 'Four Wheeler'),
                                   ('commercial', 'Commercial Vehicle'),
                                   ('heavy', 'Heavy Vehicle'),
                               ],
                               validators=[Optional()])
    permit_rc    = StringField('Permit / RC Number', validators=[Optional()])
    password         = PasswordField('Create Password',
                                     validators=[DataRequired(), strong_password])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password', message='Passwords do not match.')
                                     ])
    cb_accuracy = BooleanField('Accuracy confirmation',
                               validators=[DataRequired(message='You must confirm accuracy of details.')])
    cb_terms    = BooleanField('Terms & Conditions',
                               validators=[DataRequired(message='You must agree to the Terms & Conditions.')])
    captcha  = StringField('Captcha',
                           validators=[DataRequired(message='Captcha is required.')])
    submit = SubmitField('Create Account')
class OtpVerifyForm(FlaskForm):
    otp   = HiddenField('OTP', validators=[DataRequired()])
    phone = HiddenField('Phone')
    submit = SubmitField('Verify OTP')
class MpinSetupForm(FlaskForm):
    mpin         = HiddenField('MPIN', validators=[
        DataRequired(),
        Length(min=4, max=6, message='MPIN must be 4–6 digits.'),
        Regexp(r'^\d{4,6}$', message='MPIN must contain only digits.')
    ])
    confirm_mpin = HiddenField('Confirm MPIN', validators=[
        DataRequired(),
        EqualTo('mpin', message='MPINs do not match.')
    ])
    submit = SubmitField('Set MPIN')
class ForgotPasswordForm(FlaskForm):
    email  = StringField('Registered Email Address',
                         validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')
class ResetPasswordForm(FlaskForm):
    new_password     = PasswordField('New Password',
                                     validators=[DataRequired(), strong_password])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('new_password', message='Passwords do not match.')
                                     ])
    submit = SubmitField('Update Password')

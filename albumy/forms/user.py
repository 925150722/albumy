from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, PasswordField, TextAreaField, StringField, BooleanField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, Optional, Email, EqualTo
from flask_login import current_user
from albumy.models import User


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    username = StringField('Username', validators=[DataRequired(), Length(1, 20),
                           Regexp('^[a-zA-Z0-9]*$', message='The username should contain only a-z and A-Z and 0-9')])
    website = StringField('Website', validators=[Optional(), Length(0, 255)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(0, 120)])
    location = StringField('City', validators=[DataRequired(), Length(0, 50)])
    submit = SubmitField()

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use')


class EditEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField()


class UploadAvatarForm(FlaskForm):
    image = FileField('Upload ', validators=[FileRequired(),
                      FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png')])
    submit = SubmitField()


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('Crop and Update')


class NotificationSettingForm(FlaskForm):
    receiver_comment_notification = BooleanField('New comment')
    receiver_follow_notification = BooleanField('New follower')
    receiver_collect_notification = BooleanField('New collect')
    submit = SubmitField()


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Nw Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField()


class PrivacySettingsForm(FlaskForm):
    public_collections = BooleanField('Public my collection')
    submit = SubmitField()


class DeleteAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField()

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('Wrong username')

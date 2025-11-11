from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Optional

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])

class ContentFieldForm(FlaskForm):
    value = TextAreaField('Content')
    image_id = IntegerField('Image ID', validators=[Optional()])

class ImageUploadForm(FlaskForm):
    image = FileField('Image', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    alt_text = StringField('Alt Text', validators=[Optional(), Length(max=255)])

class ImageCropForm(FlaskForm):
    x = IntegerField('X', validators=[DataRequired()])
    y = IntegerField('Y', validators=[DataRequired()])
    width = IntegerField('Width', validators=[DataRequired()])
    height = IntegerField('Height', validators=[DataRequired()])
    image_id = HiddenField('Image ID', validators=[DataRequired()])

class SiteSettingForm(FlaskForm):
    value = TextAreaField('Value', validators=[DataRequired()])

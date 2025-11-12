from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SelectField, IntegerField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

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


class BlogArticleForm(FlaskForm):
    """Form for creating/editing blog articles"""
    slug = StringField('Slug (URL)', validators=[DataRequired(), Length(max=200)])
    
    # French fields
    title_fr = StringField('Titre (FR)', validators=[DataRequired(), Length(max=300)])
    excerpt_fr = TextAreaField('Extrait (FR)', validators=[Optional()])
    content_fr = TextAreaField('Contenu HTML (FR)', validators=[DataRequired()])
    category_fr = StringField('Catégorie (FR)', validators=[Optional(), Length(max=100)])
    tags_fr = StringField('Tags (FR) - séparés par virgules', validators=[Optional()])
    meta_title_fr = StringField('Meta Title (FR)', validators=[Optional(), Length(max=200)])
    meta_description_fr = TextAreaField('Meta Description (FR)', validators=[Optional()])
    meta_keywords_fr = StringField('Meta Keywords (FR)', validators=[Optional()])
    
    # English fields
    title_en = StringField('Title (EN)', validators=[DataRequired(), Length(max=300)])
    excerpt_en = TextAreaField('Excerpt (EN)', validators=[Optional()])
    content_en = TextAreaField('HTML Content (EN)', validators=[DataRequired()])
    category_en = StringField('Category (EN)', validators=[Optional(), Length(max=100)])
    tags_en = StringField('Tags (EN) - comma separated', validators=[Optional()])
    meta_title_en = StringField('Meta Title (EN)', validators=[Optional(), Length(max=200)])
    meta_description_en = TextAreaField('Meta Description (EN)', validators=[Optional()])
    meta_keywords_en = StringField('Meta Keywords (EN)', validators=[Optional()])
    
    # Other fields
    featured_image_id = IntegerField('Featured Image ID', validators=[Optional()])
    author_name = StringField('Author Name', validators=[Optional(), Length(max=100)])
    is_published = BooleanField('Published')


class TestimonialForm(FlaskForm):
    """Form for creating/editing testimonials"""
    client_name = StringField('Client Name', validators=[DataRequired(), Length(max=150)])
    client_company = StringField('Company', validators=[Optional(), Length(max=200)])
    
    # Bilingual client title
    client_title_fr = StringField('Titre du Client (FR)', validators=[Optional(), Length(max=200)])
    client_title_en = StringField('Client Title (EN)', validators=[Optional(), Length(max=200)])
    
    # Bilingual content
    content_fr = TextAreaField('Témoignage (FR)', validators=[DataRequired()])
    content_en = TextAreaField('Testimonial (EN)', validators=[DataRequired()])
    
    # Other fields
    client_photo_id = IntegerField('Client Photo ID', validators=[Optional()])
    rating = IntegerField('Rating (1-5)', validators=[Optional(), NumberRange(min=1, max=5)])
    is_featured = BooleanField('Featured')
    is_published = BooleanField('Published')
    display_order = IntegerField('Display Order', validators=[Optional()])


class ThemeSettingsForm(FlaskForm):
    """Form for theme settings"""
    theme_mode = SelectField('Theme Mode', 
                             choices=[('dark', 'Dark by Default'), 
                                     ('light', 'Light by Default'), 
                                     ('auto', 'Auto (Browser Preference)')],
                             validators=[DataRequired()])
    allow_user_toggle = BooleanField('Allow User Theme Toggle', default=True)

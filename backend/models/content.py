from datetime import datetime
from backend.models import db

class ContentSection(db.Model):
    __tablename__ = 'content_sections'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    fields = db.relationship('ContentField', backref='section', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'fields': [field.to_dict() for field in self.fields]
        }


class ContentField(db.Model):
    __tablename__ = 'content_fields'
    
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('content_sections.id'), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text)
    value_fr = db.Column(db.Text)
    value_en = db.Column(db.Text)
    field_type = db.Column(db.String(50), default='text')
    order = db.Column(db.Integer, default=0)
    image_id = db.Column(db.Integer, db.ForeignKey('image_assets.id'), nullable=True)
    button_link = db.Column(db.String(500))
    button_link_fr = db.Column(db.String(500))
    button_link_en = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    image = db.relationship('ImageAsset', backref='content_fields', lazy=True)
    
    __table_args__ = (
        db.UniqueConstraint('section_id', 'key', name='unique_section_key'),
    )
    
    def to_dict(self, lang=None):
        base_dict = {
            'id': self.id,
            'section_id': self.section_id,
            'key': self.key,
            'value': self.value,
            'value_fr': self.value_fr,
            'value_en': self.value_en,
            'field_type': self.field_type,
            'order': self.order,
            'button_link': self.button_link,
            'button_link_fr': self.button_link_fr,
            'button_link_en': self.button_link_en,
            'image': self.image.to_dict() if self.image else None
        }
        
        if lang == 'fr' and self.value_fr:
            base_dict['value'] = self.value_fr
        elif lang == 'en' and self.value_en:
            base_dict['value'] = self.value_en
        
        if lang == 'fr' and self.button_link_fr:
            base_dict['button_link'] = self.button_link_fr
        elif lang == 'en' and self.button_link_en:
            base_dict['button_link'] = self.button_link_en
        
        return base_dict


class ImageAsset(db.Model):
    __tablename__ = 'image_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), unique=True, nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    alt_text = db.Column(db.String(255))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    mime_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'original_name': self.original_name,
            'alt_text': self.alt_text,
            'width': self.width,
            'height': self.height,
            'mime_type': self.mime_type,
            'file_size': self.file_size,
            'url': f'/static/uploads/{self.file_name}',
            'uploaded_at': self.uploaded_at.isoformat()
        }


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    setting_type = db.Column(db.String(50), default='string')
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'setting_type': self.setting_type,
            'description': self.description
        }
    
    @staticmethod
    def get_setting(key, default=None):
        """Get a setting value by key"""
        setting = SiteSetting.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set_setting(key, value, setting_type='string', description=None):
        """Set or update a setting value"""
        setting = SiteSetting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.setting_type = setting_type
            if description:
                setting.description = description
        else:
            setting = SiteSetting(
                key=key,
                value=value,
                setting_type=setting_type,
                description=description
            )
            db.session.add(setting)
        db.session.commit()
        return setting


class AdminSession(db.Model):
    __tablename__ = 'admin_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_valid(self):
        return datetime.utcnow() < self.expires_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'is_valid': self.is_valid()
        }


class SeoMeta(db.Model):
    __tablename__ = 'seo_meta'
    
    id = db.Column(db.Integer, primary_key=True)
    page_slug = db.Column(db.String(100), unique=True, nullable=False)
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    meta_keywords = db.Column(db.Text)
    og_title = db.Column(db.String(200))
    og_description = db.Column(db.Text)
    og_image_id = db.Column(db.Integer, db.ForeignKey('image_assets.id'), nullable=True)
    twitter_card = db.Column(db.String(50), default='summary_large_image')
    canonical_url = db.Column(db.String(500))
    structured_data_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    og_image = db.relationship('ImageAsset', backref='seo_metas', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'page_slug': self.page_slug,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'meta_keywords': self.meta_keywords,
            'og_title': self.og_title,
            'og_description': self.og_description,
            'og_image': self.og_image.to_dict() if self.og_image else None,
            'twitter_card': self.twitter_card,
            'canonical_url': self.canonical_url,
            'structured_data_json': self.structured_data_json
        }

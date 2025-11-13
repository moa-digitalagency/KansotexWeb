from datetime import datetime
from backend.models import db


class CollectionSlide(db.Model):
    """Model for dynamically manageable collection slides"""
    __tablename__ = 'collection_slides'
    
    id = db.Column(db.Integer, primary_key=True)
    title_fr = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)
    button_text_fr = db.Column(db.String(100))
    button_text_en = db.Column(db.String(100))
    button_link = db.Column(db.String(500))
    image_id = db.Column(db.Integer, db.ForeignKey('image_assets.id'), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    is_visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    image = db.relationship('ImageAsset', backref='collection_slides', lazy=True)
    
    def to_dict(self, lang='fr'):
        """Convert to dictionary with language-specific content"""
        return {
            'id': self.id,
            'title': self.title_fr if lang == 'fr' else self.title_en,
            'description': self.description_fr if lang == 'fr' else self.description_en,
            'button_text': self.button_text_fr if lang == 'fr' else self.button_text_en,
            'button_link': self.button_link,
            'image': self.image.to_dict() if self.image else None,
            'display_order': self.display_order,
            'is_visible': self.is_visible
        }
    
    def to_dict_admin(self):
        """Convert to dictionary with all fields for admin panel"""
        return {
            'id': self.id,
            'title_fr': self.title_fr,
            'title_en': self.title_en,
            'description_fr': self.description_fr,
            'description_en': self.description_en,
            'button_text_fr': self.button_text_fr,
            'button_text_en': self.button_text_en,
            'button_link': self.button_link,
            'image': self.image.to_dict() if self.image else None,
            'image_id': self.image_id,
            'display_order': self.display_order,
            'is_visible': self.is_visible,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class SectionPanel(db.Model):
    """Model for dynamically manageable section panels (volets)"""
    __tablename__ = 'section_panels'
    
    id = db.Column(db.Integer, primary_key=True)
    title_fr = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    subtitle_fr = db.Column(db.String(300))
    subtitle_en = db.Column(db.String(300))
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)
    icon_class = db.Column(db.String(100))
    button_text_fr = db.Column(db.String(100))
    button_text_en = db.Column(db.String(100))
    button_link = db.Column(db.String(500))
    image_id = db.Column(db.Integer, db.ForeignKey('image_assets.id'), nullable=True)
    background_color = db.Column(db.String(50))
    display_order = db.Column(db.Integer, default=0)
    is_visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    image = db.relationship('ImageAsset', backref='section_panels', lazy=True)
    
    def to_dict(self, lang='fr'):
        """Convert to dictionary with language-specific content"""
        return {
            'id': self.id,
            'title': self.title_fr if lang == 'fr' else self.title_en,
            'subtitle': self.subtitle_fr if lang == 'fr' else self.subtitle_en,
            'description': self.description_fr if lang == 'fr' else self.description_en,
            'icon_class': self.icon_class,
            'button_text': self.button_text_fr if lang == 'fr' else self.button_text_en,
            'button_link': self.button_link,
            'image': self.image.to_dict() if self.image else None,
            'background_color': self.background_color,
            'display_order': self.display_order,
            'is_visible': self.is_visible
        }
    
    def to_dict_admin(self):
        """Convert to dictionary with all fields for admin panel"""
        return {
            'id': self.id,
            'title_fr': self.title_fr,
            'title_en': self.title_en,
            'subtitle_fr': self.subtitle_fr,
            'subtitle_en': self.subtitle_en,
            'description_fr': self.description_fr,
            'description_en': self.description_en,
            'icon_class': self.icon_class,
            'button_text_fr': self.button_text_fr,
            'button_text_en': self.button_text_en,
            'button_link': self.button_link,
            'image': self.image.to_dict() if self.image else None,
            'image_id': self.image_id,
            'background_color': self.background_color,
            'display_order': self.display_order,
            'is_visible': self.is_visible,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

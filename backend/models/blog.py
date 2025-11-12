from datetime import datetime
from backend.models import db
from sqlalchemy import Index


class BlogArticle(db.Model):
    __tablename__ = 'blog_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    
    # Bilingual titles
    title_fr = db.Column(db.String(300), nullable=False)
    title_en = db.Column(db.String(300), nullable=False)
    
    # Bilingual excerpts
    excerpt_fr = db.Column(db.Text)
    excerpt_en = db.Column(db.Text)
    
    # Bilingual HTML content
    content_fr = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=False)
    
    # Featured image
    featured_image_id = db.Column(db.Integer, db.ForeignKey('image_assets.id'), nullable=True)
    
    # Author info
    author_name = db.Column(db.String(100))
    
    # Categories/Tags (comma-separated)
    category_fr = db.Column(db.String(100))
    category_en = db.Column(db.String(100))
    tags_fr = db.Column(db.Text)  # comma-separated
    tags_en = db.Column(db.Text)  # comma-separated
    
    # SEO fields (bilingual)
    meta_title_fr = db.Column(db.String(200))
    meta_title_en = db.Column(db.String(200))
    meta_description_fr = db.Column(db.Text)
    meta_description_en = db.Column(db.Text)
    meta_keywords_fr = db.Column(db.Text)
    meta_keywords_en = db.Column(db.Text)
    
    # Publication status
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    
    # View counter
    view_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    featured_image = db.relationship('ImageAsset', backref='blog_articles', lazy=True)
    
    def to_dict(self, lang='fr'):
        """Convert to dictionary with language-specific content"""
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title_fr if lang == 'fr' else self.title_en,
            'excerpt': self.excerpt_fr if lang == 'fr' else self.excerpt_en,
            'content': self.content_fr if lang == 'fr' else self.content_en,
            'category': self.category_fr if lang == 'fr' else self.category_en,
            'tags': (self.tags_fr if lang == 'fr' else self.tags_en).split(',') if (self.tags_fr if lang == 'fr' else self.tags_en) else [],
            'featured_image': self.featured_image.to_dict() if self.featured_image else None,
            'author_name': self.author_name,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'meta_title': self.meta_title_fr if lang == 'fr' else self.meta_title_en,
            'meta_description': self.meta_description_fr if lang == 'fr' else self.meta_description_en,
            'meta_keywords': self.meta_keywords_fr if lang == 'fr' else self.meta_keywords_en
        }
    
    def to_dict_admin(self):
        """Convert to dictionary with all fields for admin panel"""
        return {
            'id': self.id,
            'slug': self.slug,
            'title_fr': self.title_fr,
            'title_en': self.title_en,
            'excerpt_fr': self.excerpt_fr,
            'excerpt_en': self.excerpt_en,
            'content_fr': self.content_fr,
            'content_en': self.content_en,
            'category_fr': self.category_fr,
            'category_en': self.category_en,
            'tags_fr': self.tags_fr,
            'tags_en': self.tags_en,
            'featured_image': self.featured_image.to_dict() if self.featured_image else None,
            'author_name': self.author_name,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'meta_title_fr': self.meta_title_fr,
            'meta_title_en': self.meta_title_en,
            'meta_description_fr': self.meta_description_fr,
            'meta_description_en': self.meta_description_en,
            'meta_keywords_fr': self.meta_keywords_fr,
            'meta_keywords_en': self.meta_keywords_en
        }


# Create indexes for better performance
Index('idx_blog_slug', BlogArticle.slug)
Index('idx_blog_published', BlogArticle.is_published, BlogArticle.published_at)


class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Client info
    client_name = db.Column(db.String(150), nullable=False)
    client_title_fr = db.Column(db.String(200))  # e.g., "Directeur Hôtel Luxe"
    client_title_en = db.Column(db.String(200))  # e.g., "Luxury Hotel Director"
    client_company = db.Column(db.String(200))
    client_photo_id = db.Column(db.Integer, db.ForeignKey('image_assets.id'), nullable=True)
    
    # Bilingual testimonial content
    content_fr = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=False)
    
    # Rating (1-5 stars)
    rating = db.Column(db.Integer, default=5)
    
    # Display settings
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client_photo = db.relationship('ImageAsset', backref='testimonials', lazy=True)
    
    def to_dict(self, lang='fr'):
        """Convert to dictionary with language-specific content"""
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_title': self.client_title_fr if lang == 'fr' else self.client_title_en,
            'client_company': self.client_company,
            'client_photo': self.client_photo.to_dict() if self.client_photo else None,
            'content': self.content_fr if lang == 'fr' else self.content_en,
            'rating': self.rating,
            'is_featured': self.is_featured,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat()
        }
    
    def to_dict_admin(self):
        """Convert to dictionary with all fields for admin panel"""
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_title_fr': self.client_title_fr,
            'client_title_en': self.client_title_en,
            'client_company': self.client_company,
            'client_photo': self.client_photo.to_dict() if self.client_photo else None,
            'content_fr': self.content_fr,
            'content_en': self.content_en,
            'rating': self.rating,
            'is_featured': self.is_featured,
            'is_published': self.is_published,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# Create indexes for better performance
Index('idx_testimonial_published', Testimonial.is_published, Testimonial.display_order)
Index('idx_testimonial_featured', Testimonial.is_featured)

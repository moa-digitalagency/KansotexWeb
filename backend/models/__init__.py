from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to ensure they are registered with SQLAlchemy
from backend.models.content import ContentSection, ContentField, ImageAsset, SiteSetting, AdminSession, SeoMeta
from backend.models.contact import Contact
from backend.models.blog import BlogArticle, Testimonial
from backend.models.dynamic_sections import CollectionSlide, SectionPanel

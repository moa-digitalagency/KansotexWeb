from backend.models import db
from backend.models.blog import Testimonial


class TestimonialService:
    """Service class for testimonial operations"""
    
    @staticmethod
    def get_all_testimonials(published_only=False, featured_only=False):
        """Get all testimonials"""
        query = Testimonial.query
        
        if published_only:
            query = query.filter_by(is_published=True)
        
        if featured_only:
            query = query.filter_by(is_featured=True)
        
        query = query.order_by(Testimonial.display_order.asc(), Testimonial.created_at.desc())
        
        return query.all()
    
    @staticmethod
    def get_testimonial_by_id(testimonial_id):
        """Get a single testimonial by ID"""
        return Testimonial.query.get(testimonial_id)
    
    @staticmethod
    def create_testimonial(data):
        """Create a new testimonial"""
        testimonial = Testimonial(
            client_name=data.get('client_name'),
            client_title_fr=data.get('client_title_fr'),
            client_title_en=data.get('client_title_en'),
            client_company=data.get('client_company'),
            client_photo_id=data.get('client_photo_id'),
            content_fr=data.get('content_fr'),
            content_en=data.get('content_en'),
            meta_title_fr=data.get('meta_title_fr'),
            meta_title_en=data.get('meta_title_en'),
            meta_description_fr=data.get('meta_description_fr'),
            meta_description_en=data.get('meta_description_en'),
            meta_keywords_fr=data.get('meta_keywords_fr'),
            meta_keywords_en=data.get('meta_keywords_en'),
            rating=data.get('rating', 5),
            is_featured=data.get('is_featured', False),
            is_published=data.get('is_published', True),
            display_order=data.get('display_order', 0)
        )
        
        db.session.add(testimonial)
        db.session.commit()
        return testimonial
    
    @staticmethod
    def update_testimonial(testimonial_id, data):
        """Update an existing testimonial"""
        testimonial = Testimonial.query.get(testimonial_id)
        if not testimonial:
            return None
        
        # Update fields
        for field in ['client_name', 'client_title_fr', 'client_title_en', 
                      'client_company', 'client_photo_id', 'content_fr', 'content_en',
                      'meta_title_fr', 'meta_title_en', 'meta_description_fr', 
                      'meta_description_en', 'meta_keywords_fr', 'meta_keywords_en',
                      'rating', 'is_featured', 'is_published', 'display_order']:
            if field in data:
                setattr(testimonial, field, data[field])
        
        db.session.commit()
        return testimonial
    
    @staticmethod
    def delete_testimonial(testimonial_id):
        """Delete a testimonial"""
        testimonial = Testimonial.query.get(testimonial_id)
        if not testimonial:
            return False
        
        db.session.delete(testimonial)
        db.session.commit()
        return True
    
    @staticmethod
    def reorder_testimonials(testimonial_orders):
        """Update display order for multiple testimonials
        
        Args:
            testimonial_orders: dict mapping testimonial_id to display_order
        """
        for testimonial_id, order in testimonial_orders.items():
            testimonial = Testimonial.query.get(testimonial_id)
            if testimonial:
                testimonial.display_order = order
        
        db.session.commit()
        return True


testimonial_service = TestimonialService()

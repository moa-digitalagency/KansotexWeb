from backend.models.dynamic_sections import CollectionSlide, SectionPanel
from backend.models import db


class CollectionService:
    """Service for managing collection slides"""
    
    @staticmethod
    def get_all_slides(visible_only=False):
        """Get all collection slides"""
        query = CollectionSlide.query
        if visible_only:
            query = query.filter_by(is_visible=True)
        return query.order_by(CollectionSlide.display_order).all()
    
    @staticmethod
    def get_slide_by_id(slide_id):
        """Get a collection slide by ID"""
        return CollectionSlide.query.get(slide_id)
    
    @staticmethod
    def create_slide(data):
        """Create a new collection slide"""
        slide = CollectionSlide(
            title_fr=data['title_fr'],
            title_en=data['title_en'],
            description_fr=data.get('description_fr', ''),
            description_en=data.get('description_en', ''),
            button_text_fr=data.get('button_text_fr', ''),
            button_text_en=data.get('button_text_en', ''),
            button_link=data.get('button_link', ''),
            image_id=data.get('image_id'),
            display_order=data.get('display_order', 0),
            is_visible=data.get('is_visible', True)
        )
        db.session.add(slide)
        db.session.commit()
        return slide
    
    @staticmethod
    def update_slide(slide_id, data):
        """Update a collection slide"""
        slide = CollectionSlide.query.get(slide_id)
        if not slide:
            return None
        
        slide.title_fr = data.get('title_fr', slide.title_fr)
        slide.title_en = data.get('title_en', slide.title_en)
        slide.description_fr = data.get('description_fr', slide.description_fr)
        slide.description_en = data.get('description_en', slide.description_en)
        slide.button_text_fr = data.get('button_text_fr', slide.button_text_fr)
        slide.button_text_en = data.get('button_text_en', slide.button_text_en)
        slide.button_link = data.get('button_link', slide.button_link)
        slide.image_id = data.get('image_id', slide.image_id)
        slide.display_order = data.get('display_order', slide.display_order)
        slide.is_visible = data.get('is_visible', slide.is_visible)
        
        db.session.commit()
        return slide
    
    @staticmethod
    def delete_slide(slide_id):
        """Delete a collection slide"""
        slide = CollectionSlide.query.get(slide_id)
        if slide:
            db.session.delete(slide)
            db.session.commit()
            return True
        return False


class PanelService:
    """Service for managing section panels (volets)"""
    
    @staticmethod
    def get_all_panels(visible_only=False):
        """Get all section panels"""
        query = SectionPanel.query
        if visible_only:
            query = query.filter_by(is_visible=True)
        return query.order_by(SectionPanel.display_order).all()
    
    @staticmethod
    def get_panel_by_id(panel_id):
        """Get a section panel by ID"""
        return SectionPanel.query.get(panel_id)
    
    @staticmethod
    def create_panel(data):
        """Create a new section panel"""
        panel = SectionPanel(
            title_fr=data['title_fr'],
            title_en=data['title_en'],
            subtitle_fr=data.get('subtitle_fr', ''),
            subtitle_en=data.get('subtitle_en', ''),
            description_fr=data.get('description_fr', ''),
            description_en=data.get('description_en', ''),
            icon_class=data.get('icon_class', 'fa-star'),
            button_text_fr=data.get('button_text_fr', ''),
            button_text_en=data.get('button_text_en', ''),
            button_link=data.get('button_link', ''),
            image_id=data.get('image_id'),
            background_color=data.get('background_color', ''),
            display_order=data.get('display_order', 0),
            is_visible=data.get('is_visible', True)
        )
        db.session.add(panel)
        db.session.commit()
        return panel
    
    @staticmethod
    def update_panel(panel_id, data):
        """Update a section panel"""
        panel = SectionPanel.query.get(panel_id)
        if not panel:
            return None
        
        panel.title_fr = data.get('title_fr', panel.title_fr)
        panel.title_en = data.get('title_en', panel.title_en)
        panel.subtitle_fr = data.get('subtitle_fr', panel.subtitle_fr)
        panel.subtitle_en = data.get('subtitle_en', panel.subtitle_en)
        panel.description_fr = data.get('description_fr', panel.description_fr)
        panel.description_en = data.get('description_en', panel.description_en)
        panel.icon_class = data.get('icon_class', panel.icon_class)
        panel.button_text_fr = data.get('button_text_fr', panel.button_text_fr)
        panel.button_text_en = data.get('button_text_en', panel.button_text_en)
        panel.button_link = data.get('button_link', panel.button_link)
        panel.image_id = data.get('image_id', panel.image_id)
        panel.background_color = data.get('background_color', panel.background_color)
        panel.display_order = data.get('display_order', panel.display_order)
        panel.is_visible = data.get('is_visible', panel.is_visible)
        
        db.session.commit()
        return panel
    
    @staticmethod
    def delete_panel(panel_id):
        """Delete a section panel"""
        panel = SectionPanel.query.get(panel_id)
        if panel:
            db.session.delete(panel)
            db.session.commit()
            return True
        return False

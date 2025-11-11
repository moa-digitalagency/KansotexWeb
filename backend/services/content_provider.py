from backend.models.content import ContentSection, ContentField

class ContentProvider:
    @staticmethod
    def get_section_content(slug):
        section = ContentSection.query.filter_by(slug=slug).first()
        if not section:
            return {}
        
        content = {}
        for field in section.fields:
            content[field.key] = {
                'value': field.value,
                'type': field.field_type,
                'image': field.image.to_dict() if field.image else None
            }
        
        return content
    
    @staticmethod
    def get_all_content():
        sections = ContentSection.query.all()
        all_content = {}
        
        for section in sections:
            all_content[section.slug] = ContentProvider.get_section_content(section.slug)
        
        return all_content
    
    @staticmethod
    def get_field(slug, key, default=''):
        section = ContentSection.query.filter_by(slug=slug).first()
        if not section:
            return default
        
        field = ContentField.query.filter_by(section_id=section.id, key=key).first()
        return field.value if field else default

content_provider = ContentProvider()

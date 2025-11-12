from backend.models import db
from backend.models.content import ContentSection, ContentField, SiteSetting

def build_section_payload(section):
    """Serialize section data for API responses"""
    if not section:
        return None
    
    fields = {}
    for field in section.fields:
        fields[field.key] = {
            'id': field.id,
            'type': field.field_type,
            'value': field.value or '',
            'image': field.image.to_dict() if field.image else None
        }
    
    return {
        'id': section.id,
        'slug': section.slug,
        'name': section.name,
        'description': section.description,
        'fields': fields
    }

class ContentService:
    @staticmethod
    def get_all_sections():
        return ContentSection.query.order_by(ContentSection.name).all()
    
    @staticmethod
    def get_section_by_slug(slug):
        return ContentSection.query.filter_by(slug=slug).first()
    
    @staticmethod
    def create_section(slug, name, description=None):
        section = ContentSection(slug=slug, name=name, description=description)
        db.session.add(section)
        db.session.commit()
        return section
    
    @staticmethod
    def update_field(section_id, key, value, field_type='text', image_id=None):
        field = ContentField.query.filter_by(section_id=section_id, key=key).first()
        
        if field:
            field.value = value
            field.field_type = field_type
            field.image_id = image_id
        else:
            field = ContentField(
                section_id=section_id,
                key=key,
                value=value,
                field_type=field_type,
                image_id=image_id
            )
            db.session.add(field)
        
        db.session.commit()
        return field
    
    @staticmethod
    def get_field_value(section_slug, key, default=''):
        section = ContentSection.query.filter_by(slug=section_slug).first()
        if not section:
            return default
        
        field = ContentField.query.filter_by(section_id=section.id, key=key).first()
        return field.value if field else default
    
    @staticmethod
    def get_section_fields(section_slug):
        section = ContentSection.query.filter_by(slug=section_slug).first()
        if not section:
            return {}
        
        fields = ContentField.query.filter_by(section_id=section.id).order_by(ContentField.order).all()
        return {field.key: field for field in fields}
    
    @staticmethod
    def get_setting(key, default=''):
        setting = SiteSetting.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def update_setting(key, value, setting_type='string', description=None):
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

content_service = ContentService()

from backend.models.content import ContentSection, ContentField, SiteSetting, SeoMeta

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
    
    @staticmethod
    def get_site_settings():
        settings = SiteSetting.query.all()
        settings_dict = {}
        for setting in settings:
            settings_dict[setting.key] = {
                'value': setting.value,
                'type': setting.setting_type,
                'description': setting.description
            }
        return settings_dict
    
    @staticmethod
    def get_seo_meta(page_slug='home'):
        seo = SeoMeta.query.filter_by(page_slug=page_slug).first()
        if not seo:
            settings = ContentProvider.get_site_settings()
            return {
                'meta_title': settings.get('default_meta_title', {}).get('value', 'KANSOTEX'),
                'meta_description': settings.get('default_meta_description', {}).get('value', ''),
                'meta_keywords': settings.get('default_meta_keywords', {}).get('value', ''),
                'og_title': settings.get('default_meta_title', {}).get('value', 'KANSOTEX'),
                'og_description': settings.get('default_meta_description', {}).get('value', ''),
                'og_image': None,
                'twitter_card': 'summary_large_image',
                'canonical_url': '',
                'structured_data_json': ''
            }
        return seo.to_dict()
    
    @staticmethod
    def get_complete_context(page_slug='home'):
        return {
            'content': ContentProvider.get_all_content(),
            'settings': ContentProvider.get_site_settings(),
            'seo': ContentProvider.get_seo_meta(page_slug)
        }

content_provider = ContentProvider()

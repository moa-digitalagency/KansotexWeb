from backend.models.content import ContentSection, ContentField, SiteSetting

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
    def get_setting_value(key, default=''):
        setting = SiteSetting.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def get_seo_meta(page_slug='home'):
        return {
            'meta_title': ContentProvider.get_setting_value('meta_title', 'KANSOTEX - Expert en Textiles de Qualité Premium'),
            'meta_description': ContentProvider.get_setting_value('meta_description', 'Expert en textiles de qualité premium'),
            'meta_keywords': ContentProvider.get_setting_value('meta_keywords', 'textiles premium, linge hôtelier, textiles médicaux'),
            'og_title': ContentProvider.get_setting_value('og_title', 'KANSOTEX'),
            'og_description': ContentProvider.get_setting_value('og_description', ''),
            'og_image': ContentProvider.get_setting_value('og_image', ''),
            'twitter_card': ContentProvider.get_setting_value('twitter_card', 'summary_large_image'),
            'twitter_title': ContentProvider.get_setting_value('twitter_title', 'KANSOTEX'),
            'twitter_description': ContentProvider.get_setting_value('twitter_description', ''),
            'twitter_image': ContentProvider.get_setting_value('twitter_image', ''),
        }
    
    @staticmethod
    def get_complete_context(page_slug='home'):
        return {
            'content': ContentProvider.get_all_content(),
            'settings': ContentProvider.get_site_settings(),
            'seo': ContentProvider.get_seo_meta(page_slug)
        }

content_provider = ContentProvider()

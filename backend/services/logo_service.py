import json
from backend.models.content import SiteSetting
from backend.models import db


class LogoService:
    """Service for managing logo configuration"""
    
    @staticmethod
    def get_logo_config():
        """Get the logo configuration from database"""
        setting = SiteSetting.query.filter_by(key='logo_config').first()
        if setting and setting.value:
            try:
                return json.loads(setting.value)
            except:
                pass
        
        # Return default configuration
        return {
            'mode': 'text',
            'text': {
                'dark': {
                    'fr': 'KANSOTEX',
                    'en': 'KANSOTEX'
                },
                'light': {
                    'fr': 'KANSOTEX',
                    'en': 'KANSOTEX'
                }
            },
            'images': {
                'dark_id': None,
                'light_id': None
            },
            'alt_text': 'KANSOTEX Logo'
        }
    
    @staticmethod
    def update_logo_config(config_data):
        """Update the logo configuration"""
        config_json = json.dumps(config_data)
        
        setting = SiteSetting.query.filter_by(key='logo_config').first()
        if setting:
            setting.value = config_json
            setting.setting_type = 'json'
            setting.description = 'Logo configuration (text/image mode, multilingual, theme support)'
        else:
            setting = SiteSetting(
                key='logo_config',
                value=config_json,
                setting_type='json',
                description='Logo configuration (text/image mode, multilingual, theme support)'
            )
            db.session.add(setting)
        
        db.session.commit()
        return config_data
    
    @staticmethod
    def get_logo_for_display(lang='fr', theme='dark'):
        """Get the appropriate logo based on language and theme"""
        config = LogoService.get_logo_config()
        
        if config['mode'] == 'text':
            # Return text logo
            return {
                'type': 'text',
                'value': config['text'][theme][lang]
            }
        else:
            # Return image logo
            image_id = config['images'].get(f'{theme}_id')
            if image_id:
                from backend.models.content import ImageAsset
                image = ImageAsset.query.get(image_id)
                if image:
                    return {
                        'type': 'image',
                        'url': f'/static/uploads/{image.file_name}',
                        'alt': config.get('alt_text', 'Logo')
                    }
            
            # Fallback to text if image not found
            return {
                'type': 'text',
                'value': config['text'][theme][lang]
            }

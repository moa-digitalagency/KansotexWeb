from flask import Flask, request
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from config import Config
from backend.models import db
from backend.routes.main_routes import main_bp
from backend.admin import admin_bp
from backend.services.content_provider import ContentProvider
from backend.utils.translations import TRANSLATIONS, get_translation

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.config.from_object(Config)
    
    CORS(app)
    csrf = CSRFProtect(app)
    
    db.init_app(app)
    
    # Register custom Jinja filters
    app.jinja_env.filters['image_url'] = ContentProvider.get_image_url
    
    # Make translations available in all templates
    @app.context_processor
    def inject_translations():
        """Inject translations and current language into all templates"""
        current_lang = getattr(request, 'current_lang', 'fr')
        return {
            't': TRANSLATIONS,
            'current_lang': current_lang,
            'get_translation': get_translation
        }
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database tables may already exist: {e}")
        
        # Auto-seed database if empty
        from backend.models.content import ContentSection
        if ContentSection.query.count() == 0:
            print("Database is empty, seeding with initial content...")
            try:
                from backend.seed_data import init_database_content
                init_database_content()
                print("Database seeded successfully!")
            except Exception as e:
                print(f"Error seeding database: {e}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

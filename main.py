from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from config import Config
from backend.models import db
from backend.routes.main_routes import main_bp
from backend.admin import admin_bp
from backend.services.content_provider import ContentProvider

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
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database tables may already exist: {e}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

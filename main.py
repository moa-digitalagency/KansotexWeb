from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.models import db
from backend.routes.main_routes import main_bp

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.config.from_object(Config)
    
    CORS(app)
    
    db.init_app(app)
    
    app.register_blueprint(main_bp)
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

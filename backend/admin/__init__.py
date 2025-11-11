from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from backend.admin import routes

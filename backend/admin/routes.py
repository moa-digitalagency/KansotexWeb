import os
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from backend.admin import admin_bp
from backend.admin.forms import LoginForm, ContentFieldForm, ImageUploadForm, ImageCropForm
from backend.admin.services.content_service import content_service
from backend.admin.services.image_service import image_service
from backend.models import db
from backend.models.content import AdminSession

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
if not ADMIN_PASSWORD:
    raise ValueError("ADMIN_PASSWORD environment variable must be set for admin panel security")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Veuillez vous connecter pour accéder à cette page', 'error')
            return redirect(url_for('admin.login'))
        
        session_token = session.get('admin_session_token')
        if session_token:
            admin_session = AdminSession.query.filter_by(session_token=session_token).first()
            if not admin_session or not admin_session.is_valid():
                session.clear()
                flash('Votre session a expiré', 'error')
                return redirect(url_for('admin.login'))
            
            admin_session.last_activity = datetime.utcnow()
            db.session.commit()
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        if secrets.compare_digest(form.password.data, ADMIN_PASSWORD):
            session_token = secrets.token_urlsafe(32)
            
            admin_session = AdminSession(
                session_token=session_token,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')[:255],
                expires_at=datetime.utcnow() + timedelta(hours=8)
            )
            db.session.add(admin_session)
            db.session.commit()
            
            session['admin_logged_in'] = True
            session['admin_session_token'] = session_token
            session.permanent = True
            
            flash('Connexion réussie!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Mot de passe incorrect', 'error')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session_token = session.get('admin_session_token')
    if session_token:
        admin_session = AdminSession.query.filter_by(session_token=session_token).first()
        if admin_session:
            db.session.delete(admin_session)
            db.session.commit()
    
    session.clear()
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    sections = content_service.get_all_sections()
    images = image_service.get_all_images()[:10]
    
    stats = {
        'total_sections': len(sections),
        'total_images': len(images),
    }
    
    return render_template('admin/dashboard.html', sections=sections, stats=stats, recent_images=images)

@admin_bp.route('/content/<section_slug>', methods=['GET', 'POST'])
@login_required
def edit_content(section_slug):
    section = content_service.get_section_by_slug(section_slug)
    if not section:
        flash('Section non trouvée', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        existing_fields = content_service.get_section_fields(section_slug)
        
        for key in existing_fields.keys():
            field_type = request.form.get(f'{key}_type', 'text')
            
            if field_type == 'image':
                image_id_str = request.form.get(f'{key}_image_id', '')
                image_id = int(image_id_str) if image_id_str else None
                value = ''
            else:
                value = request.form.get(key, '')
                image_id = None
            
            content_service.update_field(
                section.id,
                key,
                value,
                field_type,
                image_id
            )
        
        db.session.commit()
        flash('Contenu mis à jour avec succès!', 'success')
        return redirect(url_for('admin.edit_content', section_slug=section_slug))
    
    fields = content_service.get_section_fields(section_slug)
    all_images = image_service.get_all_images()
    
    return render_template('admin/edit_content.html', section=section, fields=fields, images=all_images)

@admin_bp.route('/images', methods=['GET', 'POST'])
@login_required
def images():
    form = ImageUploadForm()
    
    if form.validate_on_submit():
        try:
            image = image_service.save_image(form.image.data, form.alt_text.data)
            flash(f'Image "{image.original_name}" téléchargée avec succès!', 'success')
            return redirect(url_for('admin.images'))
        except Exception as e:
            flash(f'Erreur lors du téléchargement: {str(e)}', 'error')
    
    all_images = image_service.get_all_images()
    return render_template('admin/images.html', form=form, images=all_images)

@admin_bp.route('/images/<int:image_id>/crop', methods=['POST'])
@login_required
def crop_image(image_id):
    try:
        x = int(request.form.get('x', 0))
        y = int(request.form.get('y', 0))
        width = int(request.form.get('width', 0))
        height = int(request.form.get('height', 0))
        
        image = image_service.crop_image(image_id, x, y, width, height)
        
        return jsonify({
            'success': True,
            'message': 'Image rognée avec succès',
            'image': image.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@admin_bp.route('/images/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_image(image_id):
    try:
        if image_service.delete_image(image_id):
            flash('Image supprimée avec succès', 'success')
        else:
            flash('Image non trouvée', 'error')
    except Exception as e:
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
    
    return redirect(url_for('admin.images'))

@admin_bp.route('/upload-crop', methods=['GET'])
@login_required
def upload_crop():
    return render_template('admin/upload_crop.html')

@admin_bp.route('/upload-cropped', methods=['POST'])
@login_required
def upload_cropped():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'Aucune image fournie'}), 400
        
        file = request.files['image']
        alt_text = request.form.get('alt_text', '')
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nom de fichier vide'}), 400
        
        image = image_service.save_image(file, alt_text)
        
        return jsonify({
            'success': True,
            'message': 'Image téléchargée avec succès',
            'image': image.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@admin_bp.route('/seo', methods=['GET', 'POST'])
@login_required
def seo_settings():
    if request.method == 'POST':
        seo_keys = [
            'meta_title', 'meta_description', 'meta_keywords', 'meta_author', 
            'canonical_url', 'meta_robots', 'favicon_url',
            'schema_type', 'schema_name', 'schema_description', 'schema_logo', 'schema_url',
            'og_title', 'og_description', 'og_image', 'og_type',
            'twitter_card', 'twitter_title', 'twitter_description', 'twitter_image', 'twitter_site'
        ]
        
        for key in seo_keys:
            value = request.form.get(key, '')
            setting_type = 'text' if key in ['meta_description', 'meta_keywords', 'og_description', 'twitter_description', 'schema_description'] else 'string'
            content_service.update_setting(key, value, setting_type)
        
        db.session.commit()
        flash('Paramètres SEO mis à jour avec succès!', 'success')
        return redirect(url_for('admin.seo_settings'))
    
    seo_settings = {}
    seo_keys = [
        'meta_title', 'meta_description', 'meta_keywords', 'meta_author', 
        'canonical_url', 'meta_robots', 'favicon_url',
        'schema_type', 'schema_name', 'schema_description', 'schema_logo', 'schema_url',
        'og_title', 'og_description', 'og_image', 'og_type',
        'twitter_card', 'twitter_title', 'twitter_description', 'twitter_image', 'twitter_site'
    ]
    
    for key in seo_keys:
        seo_settings[key] = content_service.get_setting(key, '')
    
    all_images = image_service.get_all_images()
    return render_template('admin/seo.html', seo_settings=seo_settings, images=all_images)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def site_settings():
    if request.method == 'POST':
        settings_keys = [
            'site_name', 'site_logo', 'company_address', 'company_phone',
            'company_email', 'company_ice', 'facebook_url', 'instagram_url',
            'linkedin_url', 'twitter_url'
        ]
        
        for key in settings_keys:
            value = request.form.get(key, '')
            content_service.update_setting(key, value, 'string')
        
        db.session.commit()
        flash('Paramètres du site mis à jour avec succès!', 'success')
        return redirect(url_for('admin.site_settings'))
    
    settings = {}
    settings_keys = [
        'site_name', 'site_logo', 'company_address', 'company_phone',
        'company_email', 'company_ice', 'facebook_url', 'instagram_url',
        'linkedin_url', 'twitter_url'
    ]
    
    for key in settings_keys:
        settings[key] = content_service.get_setting(key, '')
    
    return render_template('admin/settings.html', settings=settings)

import os
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from backend.admin import admin_bp
from backend.admin.forms import (LoginForm, ContentFieldForm, ImageUploadForm, ImageCropForm,
                                   BlogArticleForm, TestimonialForm, ThemeSettingsForm)
from backend.admin.services.content_service import content_service, build_section_payload
from backend.admin.services.image_service import image_service
from backend.admin.services.blog_service import blog_service
from backend.admin.services.testimonial_service import testimonial_service
from backend.services.collection_service import CollectionService, PanelService
from backend.services.logo_service import LogoService
from backend.models import db
from backend.models.content import AdminSession, SiteSetting
from backend.models.blog import BlogArticle, Testimonial

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
                value_fr = ''
                value_en = ''
                button_link = None
                button_link_fr = None
                button_link_en = None
            else:
                value_fr = request.form.get(f'{key}_fr', '')
                value_en = request.form.get(f'{key}_en', '')
                button_link = request.form.get(f'{key}_link', '')
                button_link_fr = request.form.get(f'{key}_link_fr', '')
                button_link_en = request.form.get(f'{key}_link_en', '')
                image_id = None
            
            content_service.update_field(
                section.id,
                key,
                value_fr,
                field_type,
                image_id,
                value_en=value_en,
                button_link=button_link,
                button_link_fr=button_link_fr,
                button_link_en=button_link_en
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
            'site_name', 'site_logo', 'site_favicon', 'company_address', 'company_phone',
            'company_email', 'company_ice', 'facebook_url', 'instagram_url',
            'linkedin_url', 'twitter_url', 'color_theme', 'contact_recipient_email',
            'smtp_host', 'smtp_port', 'smtp_use_tls', 'smtp_sender_email',
            'theme_mode', 'allow_user_theme_toggle', 'auto_detect_language'
        ]
        
        for key in settings_keys:
            value = request.form.get(key, '')
            
            if key == 'smtp_port':
                if value and value.strip():
                    try:
                        port_value = int(value)
                        if port_value < 1 or port_value > 65535:
                            flash('Le port SMTP doit être entre 1 et 65535. Utilisation de la valeur par défaut 587.', 'warning')
                            value = '587'
                    except ValueError:
                        flash('Le port SMTP doit être un nombre. Utilisation de la valeur par défaut 587.', 'warning')
                        value = '587'
                else:
                    value = '587'
            
            content_service.update_setting(key, value, 'string')
        
        smtp_host = request.form.get('smtp_host', '')
        contact_recipient = request.form.get('contact_recipient_email', '')
        smtp_sender = request.form.get('smtp_sender_email', '')
        
        if smtp_host and not contact_recipient:
            flash('Attention: Vous avez configuré SMTP mais aucun email destinataire. Les messages ne seront pas envoyés.', 'warning')
        
        import os
        if smtp_host and not (os.environ.get('SMTP_USERNAME') and os.environ.get('SMTP_PASSWORD')):
            flash('Attention: Les credentials SMTP (SMTP_USERNAME et SMTP_PASSWORD) ne sont pas configurés dans les Secrets.', 'warning')
        
        db.session.commit()
        flash('Paramètres du site mis à jour avec succès!', 'success')
        return redirect(url_for('admin.site_settings'))
    
    settings = {}
    settings_keys = [
        'site_name', 'site_logo', 'site_favicon', 'company_address', 'company_phone',
        'company_email', 'company_ice', 'facebook_url', 'instagram_url',
        'linkedin_url', 'twitter_url', 'color_theme', 'contact_recipient_email',
        'smtp_host', 'smtp_port', 'smtp_use_tls', 'smtp_sender_email',
        'theme_mode', 'allow_user_theme_toggle', 'auto_detect_language'
    ]
    
    default_values = {
        'color_theme': 'silver',
        'smtp_port': '587',
        'smtp_use_tls': 'true',
        'theme_mode': 'dark',
        'allow_user_theme_toggle': 'true',
        'auto_detect_language': 'true'
    }
    
    for key in settings_keys:
        settings[key] = content_service.get_setting(key, default_values.get(key, ''))
    
    return render_template('admin/settings.html', settings=settings)

@admin_bp.route('/sections', methods=['GET'])
@login_required
def edit_sections():
    sections = content_service.get_all_sections()
    return render_template('admin/edit_sections.html', sections=sections)

@admin_bp.route('/api/section/<slug>', methods=['GET'])
@login_required
def get_section_api(slug):
    section = content_service.get_section_by_slug(slug)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    
    return jsonify(build_section_payload(section))

@admin_bp.route('/api/section/<slug>', methods=['POST'])
@login_required
def update_section_api(slug):
    section = content_service.get_section_by_slug(slug)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    
    existing_fields = content_service.get_section_fields(slug)
    
    for key in existing_fields.keys():
        field_type = request.form.get(f'{key}_type', 'text')
        
        if field_type == 'image':
            image_id_str = request.form.get(f'{key}_image_id', '')
            image_id = int(image_id_str) if image_id_str else None
            value_fr = ''
            value_en = ''
            button_link = None
        else:
            value_fr = request.form.get(f'{key}_fr', '')
            value_en = request.form.get(f'{key}_en', '')
            button_link = request.form.get(f'{key}_link', '')
            image_id = None
        
        content_service.update_field(
            section.id,
            key,
            value_fr,
            field_type,
            image_id,
            value_en=value_en,
            button_link=button_link
        )
    
    db.session.commit()
    return jsonify({'success': True, 'section': build_section_payload(section)})

@admin_bp.route('/sections/edit', methods=['GET', 'POST'])
@login_required
def edit_all_sections():
    sections = content_service.get_all_sections()
    active_slug = request.args.get('active_slug') or (sections[0].slug if sections else None)
    
    active_section = None
    fields = {}
    
    if active_slug:
        active_section = content_service.get_section_by_slug(active_slug)
        if active_section:
            fields = content_service.get_section_fields(active_slug)
    
    if request.method == 'POST':
        section_slug = request.form.get('section_slug')
        if not section_slug:
            flash('Section non trouvée', 'error')
            return redirect(url_for('admin.edit_all_sections'))
        
        section = content_service.get_section_by_slug(section_slug)
        if not section:
            flash('Section non trouvée', 'error')
            return redirect(url_for('admin.edit_all_sections'))
        
        existing_fields = content_service.get_section_fields(section_slug)
        
        for key in existing_fields.keys():
            field_type = request.form.get(f'{key}_type', 'text')
            
            if field_type == 'image':
                image_id_str = request.form.get(f'{key}_image_id', '')
                image_id = int(image_id_str) if image_id_str else None
                value_fr = ''
                value_en = ''
                button_link = None
                button_link_fr = None
                button_link_en = None
            else:
                value_fr = request.form.get(f'{key}_fr', '')
                value_en = request.form.get(f'{key}_en', '')
                button_link = request.form.get(f'{key}_link', '')
                button_link_fr = request.form.get(f'{key}_link_fr', '')
                button_link_en = request.form.get(f'{key}_link_en', '')
                image_id = None
            
            content_service.update_field(
                section.id,
                key,
                value_fr,
                field_type,
                image_id,
                value_en=value_en,
                button_link=button_link,
                button_link_fr=button_link_fr,
                button_link_en=button_link_en
            )
        
        db.session.commit()
        flash('Contenu mis à jour avec succès!', 'success')
        return redirect(url_for('admin.edit_all_sections', active_slug=section_slug))
    
    return render_template('admin/edit_all_sections.html', 
                         sections=sections, 
                         active_section=active_section, 
                         fields=fields)

@admin_bp.route('/api/upload-cropped-image', methods=['POST'])
@login_required
def upload_cropped_image():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'Aucune image fournie'}), 400
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({'success': False, 'error': 'Nom de fichier vide'}), 400
        
        if not image_file.content_type.startswith('image/'):
            return jsonify({'success': False, 'error': 'Le fichier doit être une image'}), 400
        
        saved_image = image_service.save_image(image_file, alt_text='Cropped image')
        
        return jsonify({
            'success': True, 
            'image_id': saved_image.id,
            'url': saved_image.to_dict()['url']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== BLOG ROUTES =====

@admin_bp.route('/blog')
@login_required
def blog_list():
    """List all blog articles"""
    articles = blog_service.get_all_articles()
    return render_template('admin/blog_list.html', articles=articles)

@admin_bp.route('/blog/new', methods=['GET', 'POST'])
@login_required
def blog_new():
    """Create a new blog article"""
    form = BlogArticleForm()
    
    if form.validate_on_submit():
        data = {
            'slug': form.slug.data,
            'title_fr': form.title_fr.data,
            'title_en': form.title_en.data,
            'excerpt_fr': form.excerpt_fr.data,
            'excerpt_en': form.excerpt_en.data,
            'content_fr': form.content_fr.data,
            'content_en': form.content_en.data,
            'category_fr': form.category_fr.data,
            'category_en': form.category_en.data,
            'tags_fr': form.tags_fr.data,
            'tags_en': form.tags_en.data,
            'featured_image_id': form.featured_image_id.data,
            'author_name': form.author_name.data,
            'meta_title_fr': form.meta_title_fr.data,
            'meta_title_en': form.meta_title_en.data,
            'meta_description_fr': form.meta_description_fr.data,
            'meta_description_en': form.meta_description_en.data,
            'meta_keywords_fr': form.meta_keywords_fr.data,
            'meta_keywords_en': form.meta_keywords_en.data,
            'is_published': form.is_published.data
        }
        
        article = blog_service.create_article(data)
        flash(f'Article "{article.title_fr}" créé avec succès!', 'success')
        return redirect(url_for('admin.blog_list'))
    
    images = image_service.get_all_images()
    return render_template('admin/blog_edit.html', form=form, article=None, images=images)

@admin_bp.route('/blog/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def blog_edit(article_id):
    """Edit an existing blog article"""
    article = blog_service.get_article_by_id(article_id)
    if not article:
        flash('Article non trouvé', 'error')
        return redirect(url_for('admin.blog_list'))
    
    form = BlogArticleForm(obj=article)
    
    if form.validate_on_submit():
        data = {
            'slug': form.slug.data,
            'title_fr': form.title_fr.data,
            'title_en': form.title_en.data,
            'excerpt_fr': form.excerpt_fr.data,
            'excerpt_en': form.excerpt_en.data,
            'content_fr': form.content_fr.data,
            'content_en': form.content_en.data,
            'category_fr': form.category_fr.data,
            'category_en': form.category_en.data,
            'tags_fr': form.tags_fr.data,
            'tags_en': form.tags_en.data,
            'featured_image_id': form.featured_image_id.data,
            'author_name': form.author_name.data,
            'meta_title_fr': form.meta_title_fr.data,
            'meta_title_en': form.meta_title_en.data,
            'meta_description_fr': form.meta_description_fr.data,
            'meta_description_en': form.meta_description_en.data,
            'meta_keywords_fr': form.meta_keywords_fr.data,
            'meta_keywords_en': form.meta_keywords_en.data,
            'is_published': form.is_published.data
        }
        
        blog_service.update_article(article_id, data)
        flash(f'Article "{article.title_fr}" mis à jour avec succès!', 'success')
        return redirect(url_for('admin.blog_list'))
    
    images = image_service.get_all_images()
    return render_template('admin/blog_edit.html', form=form, article=article, images=images)

@admin_bp.route('/blog/<int:article_id>/delete', methods=['POST'])
@login_required
def blog_delete(article_id):
    """Delete a blog article"""
    if blog_service.delete_article(article_id):
        flash('Article supprimé avec succès!', 'success')
    else:
        flash('Article non trouvé', 'error')
    
    return redirect(url_for('admin.blog_list'))


# ===== TESTIMONIAL ROUTES =====

@admin_bp.route('/testimonials')
@login_required
def testimonials_list():
    """List all testimonials"""
    testimonials = testimonial_service.get_all_testimonials()
    return render_template('admin/testimonials_list.html', testimonials=testimonials)

@admin_bp.route('/testimonials/new', methods=['GET', 'POST'])
@login_required
def testimonial_new():
    """Create a new testimonial"""
    form = TestimonialForm()
    
    if form.validate_on_submit():
        data = {
            'client_name': form.client_name.data,
            'client_title_fr': form.client_title_fr.data,
            'client_title_en': form.client_title_en.data,
            'client_company': form.client_company.data,
            'client_photo_id': form.client_photo_id.data,
            'content_fr': form.content_fr.data,
            'content_en': form.content_en.data,
            'meta_title_fr': form.meta_title_fr.data,
            'meta_title_en': form.meta_title_en.data,
            'meta_description_fr': form.meta_description_fr.data,
            'meta_description_en': form.meta_description_en.data,
            'meta_keywords_fr': form.meta_keywords_fr.data,
            'meta_keywords_en': form.meta_keywords_en.data,
            'rating': form.rating.data or 5,
            'is_featured': form.is_featured.data,
            'is_published': form.is_published.data,
            'display_order': form.display_order.data or 0
        }
        
        testimonial = testimonial_service.create_testimonial(data)
        flash(f'Témoignage de "{testimonial.client_name}" créé avec succès!', 'success')
        return redirect(url_for('admin.testimonials_list'))
    
    images = image_service.get_all_images()
    return render_template('admin/testimonial_edit.html', form=form, testimonial=None, images=images)

@admin_bp.route('/testimonials/<int:testimonial_id>/edit', methods=['GET', 'POST'])
@login_required
def testimonial_edit(testimonial_id):
    """Edit an existing testimonial"""
    testimonial = testimonial_service.get_testimonial_by_id(testimonial_id)
    if not testimonial:
        flash('Témoignage non trouvé', 'error')
        return redirect(url_for('admin.testimonials_list'))
    
    form = TestimonialForm(obj=testimonial)
    
    if form.validate_on_submit():
        data = {
            'client_name': form.client_name.data,
            'client_title_fr': form.client_title_fr.data,
            'client_title_en': form.client_title_en.data,
            'client_company': form.client_company.data,
            'client_photo_id': form.client_photo_id.data,
            'content_fr': form.content_fr.data,
            'content_en': form.content_en.data,
            'meta_title_fr': form.meta_title_fr.data,
            'meta_title_en': form.meta_title_en.data,
            'meta_description_fr': form.meta_description_fr.data,
            'meta_description_en': form.meta_description_en.data,
            'meta_keywords_fr': form.meta_keywords_fr.data,
            'meta_keywords_en': form.meta_keywords_en.data,
            'rating': form.rating.data or 5,
            'is_featured': form.is_featured.data,
            'is_published': form.is_published.data,
            'display_order': form.display_order.data or 0
        }
        
        testimonial_service.update_testimonial(testimonial_id, data)
        flash(f'Témoignage de "{testimonial.client_name}" mis à jour avec succès!', 'success')
        return redirect(url_for('admin.testimonials_list'))
    
    images = image_service.get_all_images()
    return render_template('admin/testimonial_edit.html', form=form, testimonial=testimonial, images=images)

@admin_bp.route('/testimonials/<int:testimonial_id>/delete', methods=['POST'])
@login_required
def testimonial_delete(testimonial_id):
    """Delete a testimonial"""
    if testimonial_service.delete_testimonial(testimonial_id):
        flash('Témoignage supprimé avec succès!', 'success')
    else:
        flash('Témoignage non trouvé', 'error')
    
    return redirect(url_for('admin.testimonials_list'))


# ===== THEME SETTINGS ROUTES =====

@admin_bp.route('/theme-settings', methods=['GET', 'POST'])
@login_required
def theme_settings():
    """Manage theme settings"""
    form = ThemeSettingsForm()
    
    # Load current settings
    current_theme = SiteSetting.get_setting('theme_mode', 'dark')
    allow_toggle = SiteSetting.get_setting('allow_user_theme_toggle', 'true') == 'true'
    
    if request.method == 'GET':
        form.theme_mode.data = current_theme
        form.allow_user_toggle.data = allow_toggle
    
    if form.validate_on_submit():
        SiteSetting.set_setting('theme_mode', form.theme_mode.data, 'string', 'Default theme mode (dark/light/auto)')
        SiteSetting.set_setting('allow_user_theme_toggle', 'true' if form.allow_user_toggle.data else 'false', 'boolean', 'Allow users to toggle theme')
        
        flash('Paramètres de thème mis à jour avec succès!', 'success')
        return redirect(url_for('admin.theme_settings'))
    
    return render_template('admin/theme_settings.html', form=form)


# ===== LOGO CONFIGURATION ROUTES =====

@admin_bp.route('/logo-config', methods=['GET', 'POST'])
@login_required
def logo_config():
    """Manage logo configuration"""
    if request.method == 'POST':
        mode = request.form.get('mode', 'text')
        
        config_data = {
            'mode': mode,
            'text': {
                'dark': {
                    'fr': request.form.get('text_dark_fr', 'KANSOTEX'),
                    'en': request.form.get('text_dark_en', 'KANSOTEX')
                },
                'light': {
                    'fr': request.form.get('text_light_fr', 'KANSOTEX'),
                    'en': request.form.get('text_light_en', 'KANSOTEX')
                }
            },
            'images': {
                'dark_id': int(request.form.get('image_dark_id')) if request.form.get('image_dark_id') else None,
                'light_id': int(request.form.get('image_light_id')) if request.form.get('image_light_id') else None
            },
            'alt_text': request.form.get('alt_text', 'Logo')
        }
        
        LogoService.update_logo_config(config_data)
        flash('Configuration du logo mise à jour avec succès!', 'success')
        return redirect(url_for('admin.logo_config'))
    
    logo_config = LogoService.get_logo_config()
    images = image_service.get_all_images()
    return render_template('admin/logo_config.html', logo_config=logo_config, images=images)


# ===== COLLECTION SLIDES ROUTES =====

@admin_bp.route('/collection-slides', methods=['GET'])
@login_required
def collection_slides():
    """List all collection slides"""
    slides = CollectionService.get_all_slides()
    return render_template('admin/collection_slides.html', slides=slides)

@admin_bp.route('/collection-slides/create', methods=['GET', 'POST'])
@login_required
def collection_slide_create():
    """Create a new collection slide"""
    if request.method == 'POST':
        data = {
            'title_fr': request.form.get('title_fr', ''),
            'title_en': request.form.get('title_en', ''),
            'description_fr': request.form.get('description_fr', ''),
            'description_en': request.form.get('description_en', ''),
            'button_text_fr': request.form.get('button_text_fr', ''),
            'button_text_en': request.form.get('button_text_en', ''),
            'button_link': request.form.get('button_link', ''),
            'image_id': int(request.form.get('image_id')) if request.form.get('image_id') else None,
            'display_order': int(request.form.get('display_order', 0)),
            'is_visible': request.form.get('is_visible') == 'on'
        }
        CollectionService.create_slide(data)
        flash('Slide de collection créé avec succès!', 'success')
        return redirect(url_for('admin.collection_slides'))
    
    images = image_service.get_all_images()
    return render_template('admin/collection_slide_form.html', slide=None, images=images)

@admin_bp.route('/collection-slides/<int:slide_id>/edit', methods=['GET', 'POST'])
@login_required
def collection_slide_edit(slide_id):
    """Edit a collection slide"""
    slide = CollectionService.get_slide_by_id(slide_id)
    if not slide:
        flash('Slide non trouvé', 'error')
        return redirect(url_for('admin.collection_slides'))
    
    if request.method == 'POST':
        data = {
            'title_fr': request.form.get('title_fr', ''),
            'title_en': request.form.get('title_en', ''),
            'description_fr': request.form.get('description_fr', ''),
            'description_en': request.form.get('description_en', ''),
            'button_text_fr': request.form.get('button_text_fr', ''),
            'button_text_en': request.form.get('button_text_en', ''),
            'button_link': request.form.get('button_link', ''),
            'image_id': int(request.form.get('image_id')) if request.form.get('image_id') else None,
            'display_order': int(request.form.get('display_order', 0)),
            'is_visible': request.form.get('is_visible') == 'on'
        }
        CollectionService.update_slide(slide_id, data)
        flash('Slide de collection mis à jour avec succès!', 'success')
        return redirect(url_for('admin.collection_slides'))
    
    images = image_service.get_all_images()
    return render_template('admin/collection_slide_form.html', slide=slide, images=images)

@admin_bp.route('/collection-slides/<int:slide_id>/delete', methods=['POST'])
@login_required
def collection_slide_delete(slide_id):
    """Delete a collection slide"""
    if CollectionService.delete_slide(slide_id):
        flash('Slide de collection supprimé avec succès!', 'success')
    else:
        flash('Slide non trouvé', 'error')
    return redirect(url_for('admin.collection_slides'))


# ===== SECTION PANELS (VOLETS) ROUTES =====

@admin_bp.route('/section-panels', methods=['GET'])
@login_required
def section_panels():
    """List all section panels"""
    panels = PanelService.get_all_panels()
    return render_template('admin/section_panels.html', panels=panels)

@admin_bp.route('/section-panels/create', methods=['GET', 'POST'])
@login_required
def section_panel_create():
    """Create a new section panel"""
    if request.method == 'POST':
        data = {
            'title_fr': request.form.get('title_fr', ''),
            'title_en': request.form.get('title_en', ''),
            'subtitle_fr': request.form.get('subtitle_fr', ''),
            'subtitle_en': request.form.get('subtitle_en', ''),
            'description_fr': request.form.get('description_fr', ''),
            'description_en': request.form.get('description_en', ''),
            'icon_class': request.form.get('icon_class', 'fa-star'),
            'button_text_fr': request.form.get('button_text_fr', ''),
            'button_text_en': request.form.get('button_text_en', ''),
            'button_link': request.form.get('button_link', ''),
            'image_id': int(request.form.get('image_id')) if request.form.get('image_id') else None,
            'background_color': request.form.get('background_color', ''),
            'display_order': int(request.form.get('display_order', 0)),
            'is_visible': request.form.get('is_visible') == 'on'
        }
        PanelService.create_panel(data)
        flash('Panel créé avec succès!', 'success')
        return redirect(url_for('admin.section_panels'))
    
    images = image_service.get_all_images()
    return render_template('admin/section_panel_form.html', panel=None, images=images)

@admin_bp.route('/section-panels/<int:panel_id>/edit', methods=['GET', 'POST'])
@login_required
def section_panel_edit(panel_id):
    """Edit a section panel"""
    panel = PanelService.get_panel_by_id(panel_id)
    if not panel:
        flash('Panel non trouvé', 'error')
        return redirect(url_for('admin.section_panels'))
    
    if request.method == 'POST':
        data = {
            'title_fr': request.form.get('title_fr', ''),
            'title_en': request.form.get('title_en', ''),
            'subtitle_fr': request.form.get('subtitle_fr', ''),
            'subtitle_en': request.form.get('subtitle_en', ''),
            'description_fr': request.form.get('description_fr', ''),
            'description_en': request.form.get('description_en', ''),
            'icon_class': request.form.get('icon_class', 'fa-star'),
            'button_text_fr': request.form.get('button_text_fr', ''),
            'button_text_en': request.form.get('button_text_en', ''),
            'button_link': request.form.get('button_link', ''),
            'image_id': int(request.form.get('image_id')) if request.form.get('image_id') else None,
            'background_color': request.form.get('background_color', ''),
            'display_order': int(request.form.get('display_order', 0)),
            'is_visible': request.form.get('is_visible') == 'on'
        }
        PanelService.update_panel(panel_id, data)
        flash('Panel mis à jour avec succès!', 'success')
        return redirect(url_for('admin.section_panels'))
    
    images = image_service.get_all_images()
    return render_template('admin/section_panel_form.html', panel=panel, images=images)

@admin_bp.route('/section-panels/<int:panel_id>/delete', methods=['POST'])
@login_required
def section_panel_delete(panel_id):
    """Delete a section panel"""
    if PanelService.delete_panel(panel_id):
        flash('Panel supprimé avec succès!', 'success')
    else:
        flash('Panel non trouvé', 'error')
    return redirect(url_for('admin.section_panels'))

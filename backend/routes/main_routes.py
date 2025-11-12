from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, Response, make_response
from datetime import datetime
from backend.models import db
from backend.models.contact import Contact
from backend.models.content import SiteSetting
from backend.models.blog import BlogArticle, Testimonial
from backend.services.contact_service import ContactService
from backend.services.content_provider import content_provider
from backend.admin.services.blog_service import blog_service
from backend.admin.services.testimonial_service import testimonial_service

main_bp = Blueprint('main', __name__)
contact_service = ContactService()

@main_bp.route('/')
@main_bp.route('/<lang>')
def index(lang=None):
    if lang is None:
        lang = session.get('language', 'fr')
    
    if lang not in ['fr', 'en']:
        lang = 'fr'
    
    session['language'] = lang
    
    # Get theme settings
    theme_mode = SiteSetting.get_setting('theme_mode', 'dark')
    allow_user_toggle = SiteSetting.get_setting('allow_user_theme_toggle', 'true')
    auto_detect_language = SiteSetting.get_setting('auto_detect_language', 'true')
    
    # Get recent blog articles for homepage (returns ORM objects)
    recent_articles_orm = blog_service.get_all_articles(published_only=True, limit=3)
    
    context = content_provider.get_complete_context('home', lang=lang)
    context['current_lang'] = lang
    context['theme_mode'] = theme_mode
    context['allow_user_toggle'] = allow_user_toggle == 'true'
    context['settings'] = {'auto_detect_language': auto_detect_language}
    context['recent_articles'] = [article.to_dict(lang=lang) for article in recent_articles_orm]
    return render_template('index.html', **context)

@main_bp.route('/change-language/<lang>')
def change_language(lang):
    if lang in ['fr', 'en']:
        session['language'] = lang
    return redirect(url_for('main.index'))

@main_bp.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Aucune donnée fournie'}), 400
        
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        message = data.get('message')
        
        if not all([name, email, message]):
            return jsonify({'error': 'Le nom, l\'email et le message sont requis'}), 400
        
        contact = contact_service.create_contact(name, email, phone, message)
        
        return jsonify({
            'success': True,
            'message': 'Votre message a été envoyé avec succès!',
            'data': contact.to_dict()
        }), 201
        
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error in contact form submission: {str(e)}")
        # Return a generic error message to the client
        return jsonify({
            'error': 'Une erreur est survenue lors de l\'envoi de votre message. Veuillez réessayer plus tard.'
        }), 500

# ===== BLOG ROUTES =====

@main_bp.route('/<lang>/blog')
@main_bp.route('/blog')
def blog_list(lang=None):
    """Display blog articles list"""
    if lang is None:
        lang = session.get('language', 'fr')
    
    if lang not in ['fr', 'en']:
        lang = 'fr'
    
    session['language'] = lang
    
    # Get published articles
    articles = blog_service.get_all_articles(published_only=True, limit=20)
    
    # Get theme settings
    theme_mode = SiteSetting.get_setting('theme_mode', 'dark')
    allow_user_toggle = SiteSetting.get_setting('allow_user_theme_toggle', 'true')
    
    # Get context for navbar, footer, etc.
    context = content_provider.get_complete_context('home', lang=lang)
    context['current_lang'] = lang
    context['articles'] = [article.to_dict(lang=lang) for article in articles]
    context['theme_mode'] = theme_mode
    context['allow_user_toggle'] = allow_user_toggle == 'true'
    
    return render_template('blog_list.html', **context)

@main_bp.route('/<lang>/blog/<slug>')
@main_bp.route('/blog/<slug>')
def blog_article(slug, lang=None):
    """Display a single blog article"""
    if lang is None:
        lang = session.get('language', 'fr')
    
    if lang not in ['fr', 'en']:
        lang = 'fr'
    
    session['language'] = lang
    
    # Get article
    article = blog_service.get_article_by_slug(slug)
    
    if not article or not article.is_published:
        return render_template('404.html'), 404
    
    # Increment view count
    blog_service.increment_view_count(article.id)
    
    # Get related articles
    related_articles = blog_service.get_related_articles(article, limit=3)
    
    # Get theme settings
    theme_mode = SiteSetting.get_setting('theme_mode', 'dark')
    allow_user_toggle = SiteSetting.get_setting('allow_user_theme_toggle', 'true')
    
    # Get context for navbar, footer, etc.
    context = content_provider.get_complete_context('home', lang=lang)
    context['current_lang'] = lang
    context['article'] = article.to_dict(lang=lang)
    context['related_articles'] = [a.to_dict(lang=lang) for a in related_articles]
    context['theme_mode'] = theme_mode
    context['allow_user_toggle'] = allow_user_toggle == 'true'
    
    # SEO meta for the article
    context['seo'] = {
        'meta_title': article.meta_title_fr if lang == 'fr' else article.meta_title_en,
        'meta_description': article.meta_description_fr if lang == 'fr' else article.meta_description_en,
        'meta_keywords': article.meta_keywords_fr if lang == 'fr' else article.meta_keywords_en,
        'og_title': article.meta_title_fr if lang == 'fr' else article.meta_title_en,
        'og_description': article.meta_description_fr if lang == 'fr' else article.meta_description_en,
        'og_image': article.featured_image.to_dict()['url'] if article.featured_image else None
    }
    
    return render_template('blog_article.html', **context)


# ===== TESTIMONIALS API =====

@main_bp.route('/api/testimonials')
def get_testimonials():
    """Get testimonials for display on homepage"""
    lang = request.args.get('lang', session.get('language', 'fr'))
    
    if lang not in ['fr', 'en']:
        lang = 'fr'
    
    testimonials = testimonial_service.get_all_testimonials(published_only=True)
    
    return jsonify({
        'success': True,
        'testimonials': [t.to_dict(lang=lang) for t in testimonials]
    })


# ===== SEO ROUTES =====

@main_bp.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap for search engines"""
    pages = []
    
    base_url = request.url_root.rstrip('/')
    today = datetime.now().strftime('%Y-%m-%d')
    
    static_pages = [
        {'loc': base_url + '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': base_url + '/fr', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': base_url + '/en', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': base_url + '/blog', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': base_url + '/fr/blog', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': base_url + '/en/blog', 'priority': '0.9', 'changefreq': 'daily'},
    ]
    
    for page in static_pages:
        pages.append(page)
    
    articles = blog_service.get_all_articles(published_only=True)
    for article in articles:
        pages.append({
            'loc': base_url + f'/blog/{article.slug}',
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': article.updated_at.strftime('%Y-%m-%d') if article.updated_at else today
        })
        pages.append({
            'loc': base_url + f'/fr/blog/{article.slug}',
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': article.updated_at.strftime('%Y-%m-%d') if article.updated_at else today
        })
        pages.append({
            'loc': base_url + f'/en/blog/{article.slug}',
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': article.updated_at.strftime('%Y-%m-%d') if article.updated_at else today
        })
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{page["loc"]}</loc>\n'
        if 'lastmod' in page:
            sitemap_xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        sitemap_xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        sitemap_xml += f'    <priority>{page["priority"]}</priority>\n'
        sitemap_xml += '  </url>\n'
    
    sitemap_xml += '</urlset>'
    
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

@main_bp.route('/robots.txt')
def robots():
    """Generate robots.txt for search engine crawlers"""
    base_url = request.url_root.rstrip('/')
    
    robots_txt = f"""User-agent: *
Allow: /
Allow: /fr
Allow: /en
Allow: /blog
Allow: /fr/blog
Allow: /en/blog
Allow: /static/

Disallow: /admin
Disallow: /admin/*
Disallow: /api/

Sitemap: {base_url}/sitemap.xml
"""
    
    response = make_response(robots_txt)
    response.headers['Content-Type'] = 'text/plain'
    return response

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from backend.models import db
from backend.models.contact import Contact
from backend.services.contact_service import ContactService
from backend.services.content_provider import content_provider

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
    
    context = content_provider.get_complete_context('home', lang=lang)
    context['current_lang'] = lang
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

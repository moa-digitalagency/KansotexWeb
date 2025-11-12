"""
Translations dictionary for bilingual support (French/English)
"""

TRANSLATIONS = {
    # Navigation
    'nav': {
        'home': {'fr': 'Accueil', 'en': 'Home'},
        'collection': {'fr': 'Collection', 'en': 'Collection'},
        'volets': {'fr': 'Nos Volets', 'en': 'Our Ranges'},
        'forces': {'fr': 'Points Forts', 'en': 'Strengths'},
        'engagement': {'fr': 'Engagement', 'en': 'Commitment'},
        'contact': {'fr': 'Contact', 'en': 'Contact'},
    },
    
    # Hero Section
    'hero': {
        'slide_alt': {'fr': 'Image de présentation', 'en': 'Presentation image'},
    },
    
    # Collection Section
    'collection': {
        'previous': {'fr': 'Précédent', 'en': 'Previous'},
        'next': {'fr': 'Suivant', 'en': 'Next'},
        'view_more': {'fr': 'Voir Plus', 'en': 'View More'},
    },
    
    # Volets Section
    'volets': {
        'discover': {'fr': 'Découvrir', 'en': 'Discover'},
    },
    
    # Contact Section
    'contact': {
        'form_name': {'fr': 'Nom complet', 'en': 'Full Name'},
        'form_email': {'fr': 'Email', 'en': 'Email'},
        'form_phone': {'fr': 'Téléphone', 'en': 'Phone'},
        'form_message': {'fr': 'Message', 'en': 'Message'},
        'form_submit': {'fr': 'Envoyer le message', 'en': 'Send Message'},
        'form_sending': {'fr': 'Envoi en cours...', 'en': 'Sending...'},
        'success_title': {'fr': 'Message envoyé !', 'en': 'Message Sent!'},
        'success_message': {'fr': 'Nous vous répondrons dans les plus brefs délais.', 'en': 'We will respond to you as soon as possible.'},
        'error_title': {'fr': 'Erreur', 'en': 'Error'},
        'error_message': {'fr': 'Une erreur est survenue. Veuillez réessayer.', 'en': 'An error occurred. Please try again.'},
    },
    
    # Footer
    'footer': {
        'about_title': {'fr': 'À Propos', 'en': 'About'},
        'quick_links': {'fr': 'Liens Rapides', 'en': 'Quick Links'},
        'social_media': {'fr': 'Réseaux Sociaux', 'en': 'Social Media'},
        'contact_title': {'fr': 'Contact', 'en': 'Contact'},
        'rights': {'fr': 'Tous droits réservés.', 'en': 'All rights reserved.'},
    },
    
    # Language Switcher
    'language': {
        'switch': {'fr': 'Changer de langue', 'en': 'Switch Language'},
        'french': {'fr': 'Français', 'en': 'French'},
        'english': {'fr': 'Anglais', 'en': 'English'},
    },
    
    # Admin Panel
    'admin': {
        'login_title': {'fr': 'Connexion Administrateur', 'en': 'Admin Login'},
        'password': {'fr': 'Mot de passe', 'en': 'Password'},
        'login_button': {'fr': 'Se connecter', 'en': 'Log In'},
        'logout': {'fr': 'Déconnexion', 'en': 'Logout'},
        'dashboard': {'fr': 'Tableau de bord', 'en': 'Dashboard'},
        'edit_sections': {'fr': 'Édition des Sections', 'en': 'Edit Sections'},
        'manage_images': {'fr': 'Gestion des Images', 'en': 'Manage Images'},
        'upload_crop': {'fr': 'Upload & Recadrage', 'en': 'Upload & Crop'},
        'statistics': {'fr': 'Statistiques', 'en': 'Statistics'},
        'total_sections': {'fr': 'Sections totales', 'en': 'Total Sections'},
        'total_images': {'fr': 'Images totales', 'en': 'Total Images'},
        'contacts_received': {'fr': 'Messages reçus', 'en': 'Messages Received'},
        'quick_actions': {'fr': 'Actions Rapides', 'en': 'Quick Actions'},
        'edit_content': {'fr': 'Éditer le contenu', 'en': 'Edit Content'},
        'upload_images': {'fr': 'Uploader des images', 'en': 'Upload Images'},
        'view_contacts': {'fr': 'Voir les messages', 'en': 'View Messages'},
        'sections_list': {'fr': 'Liste des Sections', 'en': 'Sections List'},
        'select_section': {'fr': 'Sélectionnez une section à gauche', 'en': 'Select a section on the left'},
        'french_content': {'fr': 'Contenu Français', 'en': 'French Content'},
        'english_content': {'fr': 'Contenu Anglais', 'en': 'English Content'},
        'button_link': {'fr': 'Lien du bouton', 'en': 'Button Link'},
        'save_changes': {'fr': 'Enregistrer les modifications', 'en': 'Save Changes'},
        'current_image': {'fr': 'Image actuelle', 'en': 'Current Image'},
        'no_image': {'fr': 'Aucune image', 'en': 'No image'},
        'upload_new': {'fr': 'Uploader une nouvelle image', 'en': 'Upload New Image'},
        'image_details': {'fr': 'Détails de l\'image', 'en': 'Image Details'},
        'path': {'fr': 'Chemin', 'en': 'Path'},
        'resolution': {'fr': 'Résolution', 'en': 'Resolution'},
        'size': {'fr': 'Taille', 'en': 'Size'},
        'type': {'fr': 'Type', 'en': 'Type'},
        'delete_image': {'fr': 'Supprimer l\'image', 'en': 'Delete Image'},
        'upload_success': {'fr': 'Image uploadée avec succès', 'en': 'Image uploaded successfully'},
        'update_success': {'fr': 'Contenu mis à jour avec succès !', 'en': 'Content updated successfully!'},
        'section_not_found': {'fr': 'Section non trouvée', 'en': 'Section not found'},
        'all_sections': {'fr': 'Toutes les sections', 'en': 'All Sections'},
    },
}

def get_translation(key_path, lang='fr'):
    """
    Get translation for a given key path and language
    Example: get_translation('nav.home', 'en') returns 'Home'
    """
    keys = key_path.split('.')
    value = TRANSLATIONS
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return key_path  # Return key if not found
    
    if isinstance(value, dict) and lang in value:
        return value[lang]
    
    return key_path  # Return key if not found


def get_translations_dict(lang='fr'):
    """
    Get all translations for a specific language in a flattened structure
    """
    result = {}
    
    def flatten(d, parent_key=''):
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                if 'fr' in v and 'en' in v:
                    result[new_key] = v.get(lang, v.get('fr', ''))
                else:
                    flatten(v, new_key)
    
    flatten(TRANSLATIONS)
    return result

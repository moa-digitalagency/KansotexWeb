from backend.models import db
from backend.models.content import ContentSection, ContentField, SiteSetting

def init_database_content():
    """Initialize database with default content - called from main.py"""
    
    print("Seeding complete content...")
    
    sections_data = [
        {
            'slug': 'hero',
            'name': 'Section Héro',
            'description': 'Bannière principale de la page d\'accueil',
            'fields': {
                'tagline': ('text', 'EXCELLENCE DEPUIS 2005'),
                'title': ('text', 'KANSOTEX'),
                'subtitle': ('text', 'Expert en Textiles de Qualité Premium'),
                'badge_1_icon': ('text', 'star'),
                'badge_1_text': ('text', '+20 ans d\'expertise'),
                'badge_2_icon': ('text', 'award'),
                'badge_2_text': ('text', 'Qualité Premium'),
                'cta_text': ('text', 'Découvrir nos atouts'),
                'slider_image_1': ('image', 'images/hotel-textile.jpg'),
                'slider_image_2': ('image', 'images/medical-textile.jpg'),
                'slider_image_3': ('image', 'images/literie.jpg'),
            }
        },
        {
            'slug': 'forces',
            'name': 'Points Forts',
            'description': 'Section des points forts de l\'entreprise',
            'fields': {
                'title': ('text', 'Nos Points Forts'),
                'description': ('text', 'Ce qui nous distingue dans l\'univers des textiles de qualité premium'),
                'strength_1_title': ('text', 'Expérience Significative'),
                'strength_1_text': ('text', 'Une expérience significative dans l\'accompagnement des professionnels désireux de se distinguer grâce à un travail de qualité alliant un choix méticuleux des tissus.'),
                'strength_2_title': ('text', 'Compréhension Parfaite'),
                'strength_2_text': ('text', 'Une parfaite compréhension des besoins des professionnels et des particuliers, ce qui nous permet de donner vie à vos projets.'),
                'strength_3_title': ('text', 'Personnalisation Expert'),
                'strength_3_text': ('text', 'Personnalisation de vos commandes en tenant compte de votre cahier de charge et des normes techniques grâce à notre atelier.'),
                'strength_4_title': ('text', 'Rapidité d\'Exécution'),
                'strength_4_text': ('text', 'Une rapidité dans l\'exécution des commandes pour répondre à vos besoins dans les meilleurs délais.'),
                'strength_5_title': ('text', 'Livraison Rapide'),
                'strength_5_text': ('text', 'Livraison partout au Maroc dans un délai de 24h pour assurer votre satisfaction.'),
                'strength_6_title': ('text', '+20 Ans d\'Excellence'),
                'strength_6_text': ('text', 'Expert reconnu dans les textiles premium pour hôtels, cliniques et maisons. Une expérience de luxe inégalée.'),
            }
        },
        {
            'slug': 'collection',
            'name': 'Notre Collection',
            'description': 'Section collection de produits',
            'fields': {
                'title': ('text', 'Notre Collection Premium'),
                'description': ('text', 'Découvrez l\'excellence de nos textiles de luxe'),
                'slide_1_image': ('image', 'images/textile-1.jpg'),
                'slide_1_category': ('text', 'COLLECTION EXCLUSIVE'),
                'slide_1_title': ('text', 'Tissus de Luxe'),
                'slide_1_description': ('text', 'Qualité exceptionnelle pour vos projets premium'),
                'slide_2_image': ('image', 'images/textile-2.jpg'),
                'slide_2_category': ('text', 'DESIGN MODERNE'),
                'slide_2_title': ('text', 'Collection Premium'),
                'slide_2_description': ('text', 'Design moderne et élégant pour vos espaces'),
                'slide_3_image': ('image', 'images/bedding-1.jpg'),
                'slide_3_category': ('text', 'HÔTELLERIE DE LUXE'),
                'slide_3_title': ('text', 'Literie Hôtelière'),
                'slide_3_description': ('text', 'Confort 5 étoiles pour une expérience exceptionnelle'),
                'slide_4_image': ('image', 'images/serviettes.jpg'),
                'slide_4_category': ('text', 'QUALITÉ SUPÉRIEURE'),
                'slide_4_title': ('text', 'Serviettes de Luxe'),
                'slide_4_description': ('text', 'Absorption parfaite et douceur exceptionnelle'),
                'slide_5_image': ('image', 'images/bedding-2.jpg'),
                'slide_5_category': ('text', 'EXCELLENCE'),
                'slide_5_title': ('text', 'Excellence Textile'),
                'slide_5_description': ('text', 'Douceur suprême et durabilité exceptionnelle'),
                'slide_6_image': ('image', 'images/home-textile.jpg'),
                'slide_6_category': ('text', 'CONFORT MAISON'),
                'slide_6_title': ('text', 'Textile Maison'),
                'slide_6_description': ('text', 'Élégance et confort pour votre intérieur'),
            }
        },
        {
            'slug': 'volets',
            'name': 'Nos Volets',
            'description': 'Nos différents secteurs d\'activité',
            'fields': {
                'title': ('text', 'Nos Volets d\'Excellence'),
                'description': ('text', 'Des solutions textiles adaptées à chaque secteur'),
                'volet_1_image': ('image', 'images/home-textile.jpg'),
                'volet_1_title': ('text', 'Home Textile'),
                'volet_1_description': ('text', 'Des textiles de maison élégants et confortables pour votre quotidien.'),
                'volet_2_image': ('image', 'images/hotel-textile.jpg'),
                'volet_2_title': ('text', 'Hotel Textile'),
                'volet_2_description': ('text', 'Solutions premium pour l\'hôtellerie de luxe et les établissements haut de gamme.'),
                'volet_3_image': ('image', 'images/medical-textile.jpg'),
                'volet_3_title': ('text', 'Medical Textile'),
                'volet_3_description': ('text', 'Textiles médicaux conformes aux normes les plus strictes pour les cliniques.'),
                'volet_4_image': ('image', 'images/literie.jpg'),
                'volet_4_title': ('text', 'Literie et Linge de Maison'),
                'volet_4_description': ('text', 'Une literie de qualité supérieure pour un sommeil réparateur.'),
                'volet_5_image': ('image', 'images/serviettes.jpg'),
                'volet_5_title': ('text', 'Serviettes et Sorties de Bain'),
                'volet_5_description': ('text', 'Serviettes douces et absorbantes pour un confort optimal.'),
                'volet_6_image': ('image', 'images/textile-3.jpg'),
                'volet_6_title': ('text', 'Textile Professionnel'),
                'volet_6_description': ('text', 'Solutions textiles sur-mesure pour les professionnels exigeants.'),
                'background_image': ('image', 'images/textile-3.jpg'),
            }
        },
        {
            'slug': 'engagement',
            'name': 'Notre Engagement',
            'description': 'Nos engagements qualité',
            'fields': {
                'title': ('text', 'Notre Engagement'),
                'description': ('text', 'Des valeurs fortes au service de votre satisfaction'),
                'pillar_1_title': ('text', 'Matériaux Haut de Gamme'),
                'pillar_1_text': ('text', 'Chez Kansotex, nous sélectionnons uniquement des tissus de première qualité, garantissant durabilité et confort exceptionnels.'),
                'pillar_2_title': ('text', 'Contrôle de Qualité Rigoureux'),
                'pillar_2_text': ('text', 'Chaque produit passe par un processus de contrôle rigoureux pour assurer une finition parfaite et une satisfaction client maximale.'),
                'pillar_3_title': ('text', 'Innovation Constante'),
                'pillar_3_text': ('text', 'Nous nous engageons à une innovation constante afin de vous offrir constamment des produits tendance et au summum du confort.'),
                'background_image': ('image', 'images/bedding-1.jpg'),
            }
        },
        {
            'slug': 'testimonials',
            'name': 'Témoignages',
            'description': 'Témoignages clients',
            'fields': {
                'title': ('text', 'Ce que disent nos clients'),
                'description': ('text', 'Découvrez l\'expérience de nos clients satisfaits'),
            }
        },
        {
            'slug': 'contact',
            'name': 'Contact',
            'description': 'Section contact et coordonnées',
            'fields': {
                'title': ('text', 'Contactez-Nous'),
                'description': ('text', 'Nous sommes à votre écoute pour répondre à toutes vos questions'),
                'company_name': ('text', 'KANSOTEX'),
                'company_description': ('text', 'Expert en Textiles de Qualité Premium'),
                'contact_ice': ('text', '001234567890123'),
                'contact_phone': ('text', '+212 5XX-XXXXXX'),
                'contact_email': ('text', 'contact@kansotex.ma'),
                'contact_address': ('text', 'Casablanca, Maroc'),
                'form_title': ('text', 'Envoyez-nous un message'),
                'form_name_placeholder': ('text', 'Votre nom complet'),
                'form_email_placeholder': ('text', 'Votre email'),
                'form_phone_placeholder': ('text', 'Votre téléphone'),
                'form_message_placeholder': ('text', 'Votre message'),
                'form_submit_text': ('text', 'Envoyer le message'),
            }
        },
        {
            'slug': 'footer',
            'name': 'Pied de page',
            'description': 'Contenu du footer',
            'fields': {
                'company_name': ('text', 'KANSOTEX'),
                'company_description': ('text', 'Expert en Textiles de Qualité Premium depuis 2005. Nous offrons des solutions textiles haut de gamme pour l\'hôtellerie, le médical et la maison.'),
                'company_tagline': ('text', 'L\'Excellence Textile à votre Service'),
                'social_label': ('text', 'Suivez-nous'),
                'social_facebook': ('text', '#'),
                'social_instagram': ('text', '#'),
                'social_linkedin': ('text', '#'),
                'background_image': ('image', 'images/textile-3.jpg'),
                'contact_title': ('text', 'Nos Coordonnées'),
                'contact_phone': ('text', '+212 5XX-XXXXXX'),
                'contact_email': ('text', 'contact@kansotex.ma'),
                'contact_address': ('text', 'Casablanca, Maroc'),
                'copyright': ('text', '© 2024 KANSOTEX. Tous droits réservés.'),
            }
        }
    ]
    
    for section_data in sections_data:
        section = ContentSection(
            slug=section_data['slug'],
            name=section_data['name'],
            description=section_data.get('description', '')
        )
        db.session.add(section)
        db.session.flush()
        
        order = 0
        for key, (field_type, value) in section_data['fields'].items():
            field = ContentField(
                section_id=section.id,
                key=key,
                value=value,
                field_type=field_type,
                order=order
            )
            db.session.add(field)
            order += 1
    
    settings_data = [
        ('meta_title', 'KANSOTEX - Expert en Textiles de Qualité Premium', 'string', 'Titre de la page pour SEO'),
        ('meta_description', 'Expert en textiles de qualité premium pour l\'hôtellerie, le médical et la maison. Solutions sur-mesure et livraison rapide partout au Maroc.', 'string', 'Description de la page pour SEO'),
        ('meta_keywords', 'textiles premium, linge hôtelier, textiles médicaux, literie de luxe, Casablanca, Maroc', 'string', 'Mots-clés pour SEO'),
        ('og_title', 'KANSOTEX - Expert en Textiles de Qualité Premium', 'string', 'Titre Open Graph'),
        ('og_description', 'Expert en textiles de qualité premium depuis 2005', 'string', 'Description Open Graph'),
        ('og_image', '/static/images/og-image.jpg', 'string', 'Image Open Graph'),
        ('twitter_card', 'summary_large_image', 'string', 'Type de carte Twitter'),
        ('twitter_title', 'KANSOTEX - Expert en Textiles Premium', 'string', 'Titre Twitter'),
        ('twitter_description', 'Expert en textiles de qualité premium depuis 2005', 'string', 'Description Twitter'),
        ('twitter_image', '/static/images/twitter-image.jpg', 'string', 'Image Twitter'),
        ('color_theme', 'gold', 'string', 'Thème de couleur du site (gold/blue)'),
    ]
    
    for key, value, setting_type, description in settings_data:
        setting = SiteSetting(
            key=key,
            value=value,
            setting_type=setting_type,
            description=description
        )
        db.session.add(setting)
    
    db.session.commit()
    print("✓ Complete content seeded successfully!")

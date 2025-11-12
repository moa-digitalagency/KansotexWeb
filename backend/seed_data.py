from backend.models import db
from backend.models.content import ContentSection, ContentField, SiteSetting

def init_database_content():
    """Initialize database with default bilingual content - called from main.py"""
    
    print("Seeding complete bilingual content...")
    
    sections_data = [
        {
            'slug': 'hero',
            'name': 'Section Héro',
            'description': 'Bannière principale de la page d\'accueil',
            'fields': {
                'tagline': {'type': 'text', 'fr': 'EXCELLENCE DEPUIS 2005', 'en': 'EXCELLENCE SINCE 2005'},
                'title': {'type': 'text', 'fr': 'KANSOTEX', 'en': 'KANSOTEX'},
                'subtitle': {'type': 'text', 'fr': 'Expert en Textiles de Qualité Premium', 'en': 'Premium Quality Textile Expert'},
                'badge_1_icon': {'type': 'text', 'fr': 'star', 'en': 'star'},
                'badge_1_text': {'type': 'text', 'fr': '+20 ans d\'expertise', 'en': '+20 years of expertise'},
                'badge_2_icon': {'type': 'text', 'fr': 'award', 'en': 'award'},
                'badge_2_text': {'type': 'text', 'fr': 'Qualité Premium', 'en': 'Premium Quality'},
                'cta_text': {'type': 'text', 'fr': 'Découvrir nos atouts', 'en': 'Discover our strengths'},
                'slider_image_1': {'type': 'image', 'fr': 'images/hotel-textile.jpg', 'en': 'images/hotel-textile.jpg'},
                'slider_image_2': {'type': 'image', 'fr': 'images/medical-textile.jpg', 'en': 'images/medical-textile.jpg'},
                'slider_image_3': {'type': 'image', 'fr': 'images/literie.jpg', 'en': 'images/literie.jpg'},
            }
        },
        {
            'slug': 'forces',
            'name': 'Points Forts',
            'description': 'Section des points forts de l\'entreprise',
            'fields': {
                'title': {'type': 'text', 'fr': 'Nos Points Forts', 'en': 'Our Strengths'},
                'description': {'type': 'text', 'fr': 'Ce qui nous distingue dans l\'univers des textiles de qualité premium', 'en': 'What distinguishes us in the world of premium quality textiles'},
                'strength_1_title': {'type': 'text', 'fr': 'Expérience Significative', 'en': 'Significant Experience'},
                'strength_1_text': {'type': 'text', 'fr': 'Une expérience significative dans l\'accompagnement des professionnels désireux de se distinguer grâce à un travail de qualité alliant un choix méticuleux des tissus.', 'en': 'Significant experience in supporting professionals who wish to distinguish themselves through quality work combining a meticulous choice of fabrics.'},
                'strength_2_title': {'type': 'text', 'fr': 'Compréhension Parfaite', 'en': 'Perfect Understanding'},
                'strength_2_text': {'type': 'text', 'fr': 'Une parfaite compréhension des besoins des professionnels et des particuliers, ce qui nous permet de donner vie à vos projets.', 'en': 'A perfect understanding of the needs of professionals and individuals, which allows us to bring your projects to life.'},
                'strength_3_title': {'type': 'text', 'fr': 'Personnalisation Expert', 'en': 'Expert Customization'},
                'strength_3_text': {'type': 'text', 'fr': 'Personnalisation de vos commandes en tenant compte de votre cahier de charge et des normes techniques grâce à notre atelier.', 'en': 'Customization of your orders taking into account your specifications and technical standards thanks to our workshop.'},
                'strength_4_title': {'type': 'text', 'fr': 'Rapidité d\'Exécution', 'en': 'Fast Execution'},
                'strength_4_text': {'type': 'text', 'fr': 'Une rapidité dans l\'exécution des commandes pour répondre à vos besoins dans les meilleurs délais.', 'en': 'Speed in order execution to meet your needs in the shortest time possible.'},
                'strength_5_title': {'type': 'text', 'fr': 'Livraison Rapide', 'en': 'Fast Delivery'},
                'strength_5_text': {'type': 'text', 'fr': 'Livraison partout au Maroc dans un délai de 24h pour assurer votre satisfaction.', 'en': 'Delivery throughout Morocco within 24 hours to ensure your satisfaction.'},
                'strength_6_title': {'type': 'text', 'fr': '+20 Ans d\'Excellence', 'en': '+20 Years of Excellence'},
                'strength_6_text': {'type': 'text', 'fr': 'Expert reconnu dans les textiles premium pour hôtels, cliniques et maisons. Une expérience de luxe inégalée.', 'en': 'Recognized expert in premium textiles for hotels, clinics and homes. An unmatched luxury experience.'},
            }
        },
        {
            'slug': 'collection',
            'name': 'Notre Collection',
            'description': 'Section collection de produits',
            'fields': {
                'title': {'type': 'text', 'fr': 'Notre Collection Premium', 'en': 'Our Premium Collection'},
                'description': {'type': 'text', 'fr': 'Découvrez l\'excellence de nos textiles de luxe', 'en': 'Discover the excellence of our luxury textiles'},
                'slide_1_image': {'type': 'image', 'fr': 'images/textile-1.jpg', 'en': 'images/textile-1.jpg'},
                'slide_1_category': {'type': 'text', 'fr': 'COLLECTION EXCLUSIVE', 'en': 'EXCLUSIVE COLLECTION'},
                'slide_1_title': {'type': 'text', 'fr': 'Tissus de Luxe', 'en': 'Luxury Fabrics'},
                'slide_1_description': {'type': 'text', 'fr': 'Qualité exceptionnelle pour vos projets premium', 'en': 'Exceptional quality for your premium projects'},
                'slide_2_image': {'type': 'image', 'fr': 'images/textile-2.jpg', 'en': 'images/textile-2.jpg'},
                'slide_2_category': {'type': 'text', 'fr': 'DESIGN MODERNE', 'en': 'MODERN DESIGN'},
                'slide_2_title': {'type': 'text', 'fr': 'Collection Premium', 'en': 'Premium Collection'},
                'slide_2_description': {'type': 'text', 'fr': 'Design moderne et élégant pour vos espaces', 'en': 'Modern and elegant design for your spaces'},
                'slide_3_image': {'type': 'image', 'fr': 'images/bedding-1.jpg', 'en': 'images/bedding-1.jpg'},
                'slide_3_category': {'type': 'text', 'fr': 'HÔTELLERIE DE LUXE', 'en': 'LUXURY HOSPITALITY'},
                'slide_3_title': {'type': 'text', 'fr': 'Literie Hôtelière', 'en': 'Hotel Bedding'},
                'slide_3_description': {'type': 'text', 'fr': 'Confort 5 étoiles pour une expérience exceptionnelle', 'en': '5-star comfort for an exceptional experience'},
                'slide_4_image': {'type': 'image', 'fr': 'images/serviettes.jpg', 'en': 'images/serviettes.jpg'},
                'slide_4_category': {'type': 'text', 'fr': 'QUALITÉ SUPÉRIEURE', 'en': 'SUPERIOR QUALITY'},
                'slide_4_title': {'type': 'text', 'fr': 'Serviettes de Luxe', 'en': 'Luxury Towels'},
                'slide_4_description': {'type': 'text', 'fr': 'Absorption parfaite et douceur exceptionnelle', 'en': 'Perfect absorption and exceptional softness'},
                'slide_5_image': {'type': 'image', 'fr': 'images/bedding-2.jpg', 'en': 'images/bedding-2.jpg'},
                'slide_5_category': {'type': 'text', 'fr': 'EXCELLENCE', 'en': 'EXCELLENCE'},
                'slide_5_title': {'type': 'text', 'fr': 'Excellence Textile', 'en': 'Textile Excellence'},
                'slide_5_description': {'type': 'text', 'fr': 'Douceur suprême et durabilité exceptionnelle', 'en': 'Supreme softness and exceptional durability'},
                'slide_6_image': {'type': 'image', 'fr': 'images/home-textile.jpg', 'en': 'images/home-textile.jpg'},
                'slide_6_category': {'type': 'text', 'fr': 'CONFORT MAISON', 'en': 'HOME COMFORT'},
                'slide_6_title': {'type': 'text', 'fr': 'Textile Maison', 'en': 'Home Textiles'},
                'slide_6_description': {'type': 'text', 'fr': 'Élégance et confort pour votre intérieur', 'en': 'Elegance and comfort for your interior'},
            }
        },
        {
            'slug': 'volets',
            'name': 'Nos Volets',
            'description': 'Nos différents secteurs d\'activité',
            'fields': {
                'title': {'type': 'text', 'fr': 'Nos Volets d\'Excellence', 'en': 'Our Ranges of Excellence'},
                'description': {'type': 'text', 'fr': 'Des solutions textiles adaptées à chaque secteur', 'en': 'Textile solutions tailored to each sector'},
                'volet_1_image': {'type': 'image', 'fr': 'images/home-textile.jpg', 'en': 'images/home-textile.jpg'},
                'volet_1_title': {'type': 'text', 'fr': 'Home Textile', 'en': 'Home Textile'},
                'volet_1_description': {'type': 'text', 'fr': 'Des textiles de maison élégants et confortables pour votre quotidien.', 'en': 'Elegant and comfortable home textiles for your daily life.'},
                'volet_2_image': {'type': 'image', 'fr': 'images/hotel-textile.jpg', 'en': 'images/hotel-textile.jpg'},
                'volet_2_title': {'type': 'text', 'fr': 'Hotel Textile', 'en': 'Hotel Textile'},
                'volet_2_description': {'type': 'text', 'fr': 'Solutions premium pour l\'hôtellerie de luxe et les établissements haut de gamme.', 'en': 'Premium solutions for luxury hospitality and high-end establishments.'},
                'volet_3_image': {'type': 'image', 'fr': 'images/medical-textile.jpg', 'en': 'images/medical-textile.jpg'},
                'volet_3_title': {'type': 'text', 'fr': 'Medical Textile', 'en': 'Medical Textile'},
                'volet_3_description': {'type': 'text', 'fr': 'Textiles médicaux conformes aux normes les plus strictes pour les cliniques.', 'en': 'Medical textiles compliant with the strictest standards for clinics.'},
                'volet_4_image': {'type': 'image', 'fr': 'images/literie.jpg', 'en': 'images/literie.jpg'},
                'volet_4_title': {'type': 'text', 'fr': 'Literie et Linge de Maison', 'en': 'Bedding and Home Linen'},
                'volet_4_description': {'type': 'text', 'fr': 'Une literie de qualité supérieure pour un sommeil réparateur.', 'en': 'Superior quality bedding for restful sleep.'},
                'volet_5_image': {'type': 'image', 'fr': 'images/serviettes.jpg', 'en': 'images/serviettes.jpg'},
                'volet_5_title': {'type': 'text', 'fr': 'Serviettes et Sorties de Bain', 'en': 'Towels and Bathrobes'},
                'volet_5_description': {'type': 'text', 'fr': 'Serviettes douces et absorbantes pour un confort optimal.', 'en': 'Soft and absorbent towels for optimal comfort.'},
                'volet_6_image': {'type': 'image', 'fr': 'images/textile-3.jpg', 'en': 'images/textile-3.jpg'},
                'volet_6_title': {'type': 'text', 'fr': 'Textile Professionnel', 'en': 'Professional Textile'},
                'volet_6_description': {'type': 'text', 'fr': 'Solutions textiles sur-mesure pour les professionnels exigeants.', 'en': 'Custom textile solutions for demanding professionals.'},
                'background_image': {'type': 'image', 'fr': 'images/textile-3.jpg', 'en': 'images/textile-3.jpg'},
            }
        },
        {
            'slug': 'engagement',
            'name': 'Notre Engagement',
            'description': 'Nos engagements qualité',
            'fields': {
                'title': {'type': 'text', 'fr': 'Notre Engagement', 'en': 'Our Commitment'},
                'description': {'type': 'text', 'fr': 'Des valeurs fortes au service de votre satisfaction', 'en': 'Strong values serving your satisfaction'},
                'pillar_1_title': {'type': 'text', 'fr': 'Matériaux Haut de Gamme', 'en': 'High-End Materials'},
                'pillar_1_text': {'type': 'text', 'fr': 'Chez Kansotex, nous sélectionnons uniquement des tissus de première qualité, garantissant durabilité et confort exceptionnels.', 'en': 'At Kansotex, we select only top-quality fabrics, guaranteeing exceptional durability and comfort.'},
                'pillar_2_title': {'type': 'text', 'fr': 'Contrôle de Qualité Rigoureux', 'en': 'Rigorous Quality Control'},
                'pillar_2_text': {'type': 'text', 'fr': 'Chaque produit passe par un processus de contrôle rigoureux pour assurer une finition parfaite et une satisfaction client maximale.', 'en': 'Each product goes through a rigorous control process to ensure a perfect finish and maximum customer satisfaction.'},
                'pillar_3_title': {'type': 'text', 'fr': 'Innovation Constante', 'en': 'Constant Innovation'},
                'pillar_3_text': {'type': 'text', 'fr': 'Nous nous engageons à une innovation constante afin de vous offrir constamment des produits tendance et au summum du confort.', 'en': 'We are committed to constant innovation to consistently offer you trendy products at the peak of comfort.'},
                'background_image': {'type': 'image', 'fr': 'images/bedding-1.jpg', 'en': 'images/bedding-1.jpg'},
            }
        },
        {
            'slug': 'testimonials',
            'name': 'Témoignages',
            'description': 'Témoignages clients',
            'fields': {
                'title': {'type': 'text', 'fr': 'Ce que disent nos clients', 'en': 'What our clients say'},
                'description': {'type': 'text', 'fr': 'Découvrez l\'expérience de nos clients satisfaits', 'en': 'Discover the experience of our satisfied clients'},
            }
        },
        {
            'slug': 'contact',
            'name': 'Contact',
            'description': 'Section contact et coordonnées',
            'fields': {
                'title': {'type': 'text', 'fr': 'Contactez-Nous', 'en': 'Contact Us'},
                'description': {'type': 'text', 'fr': 'Nous sommes à votre écoute pour répondre à toutes vos questions', 'en': 'We are here to answer all your questions'},
                'company_name': {'type': 'text', 'fr': 'KANSOTEX', 'en': 'KANSOTEX'},
                'company_description': {'type': 'text', 'fr': 'Expert en Textiles de Qualité Premium', 'en': 'Premium Quality Textile Expert'},
                'contact_ice': {'type': 'text', 'fr': '001234567890123', 'en': '001234567890123'},
                'contact_phone': {'type': 'text', 'fr': '+212 5XX-XXXXXX', 'en': '+212 5XX-XXXXXX'},
                'contact_email': {'type': 'text', 'fr': 'contact@kansotex.ma', 'en': 'contact@kansotex.ma'},
                'contact_address': {'type': 'text', 'fr': 'Casablanca, Maroc', 'en': 'Casablanca, Morocco'},
                'form_title': {'type': 'text', 'fr': 'Envoyez-nous un message', 'en': 'Send us a message'},
                'form_name_placeholder': {'type': 'text', 'fr': 'Votre nom complet', 'en': 'Your full name'},
                'form_email_placeholder': {'type': 'text', 'fr': 'Votre email', 'en': 'Your email'},
                'form_phone_placeholder': {'type': 'text', 'fr': 'Votre téléphone', 'en': 'Your phone'},
                'form_message_placeholder': {'type': 'text', 'fr': 'Votre message', 'en': 'Your message'},
                'form_submit_text': {'type': 'text', 'fr': 'Envoyer le message', 'en': 'Send message'},
            }
        },
        {
            'slug': 'footer',
            'name': 'Pied de page',
            'description': 'Contenu du footer',
            'fields': {
                'company_name': {'type': 'text', 'fr': 'KANSOTEX', 'en': 'KANSOTEX'},
                'company_description': {'type': 'text', 'fr': 'Expert en Textiles de Qualité Premium depuis 2005. Nous offrons des solutions textiles haut de gamme pour l\'hôtellerie, le médical et la maison.', 'en': 'Premium Quality Textile Expert since 2005. We offer high-end textile solutions for hospitality, medical and home.'},
                'company_tagline': {'type': 'text', 'fr': 'L\'Excellence Textile à votre Service', 'en': 'Textile Excellence at Your Service'},
                'social_label': {'type': 'text', 'fr': 'Suivez-nous', 'en': 'Follow us'},
                'social_facebook': {'type': 'text', 'fr': '#', 'en': '#'},
                'social_instagram': {'type': 'text', 'fr': '#', 'en': '#'},
                'social_linkedin': {'type': 'text', 'fr': '#', 'en': '#'},
                'background_image': {'type': 'image', 'fr': 'images/textile-3.jpg', 'en': 'images/textile-3.jpg'},
                'contact_title': {'type': 'text', 'fr': 'Nos Coordonnées', 'en': 'Our Contact Details'},
                'contact_phone': {'type': 'text', 'fr': '+212 5XX-XXXXXX', 'en': '+212 5XX-XXXXXX'},
                'contact_email': {'type': 'text', 'fr': 'contact@kansotex.ma', 'en': 'contact@kansotex.ma'},
                'contact_address': {'type': 'text', 'fr': 'Casablanca, Maroc', 'en': 'Casablanca, Morocco'},
                'copyright': {'type': 'text', 'fr': '© 2024 KANSOTEX. Tous droits réservés.', 'en': '© 2024 KANSOTEX. All rights reserved.'},
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
        for key, field_data in section_data['fields'].items():
            field_type = field_data.get('type', 'text')
            value_fr = field_data.get('fr', '')
            value_en = field_data.get('en', '')
            
            field = ContentField(
                section_id=section.id,
                key=key,
                value=value_fr,
                value_fr=value_fr,
                value_en=value_en,
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

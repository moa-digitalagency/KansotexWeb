from datetime import datetime
from backend.models import db
from backend.models.content import ContentSection, ContentField, SiteSetting, ImageAsset
from backend.models.blog import BlogArticle, Testimonial
from backend.models.dynamic_sections import CollectionSlide, SectionPanel

def init_database_content():
    """Initialize database with default bilingual content - called from main.py"""
    
    print("Seeding complete bilingual content...")
    
    # Seed blog images first
    print("Seeding blog images...")
    blog_images = [
        {
            'file_name': 'hotel-textile.jpg',
            'original_name': 'hotel-textile.jpg',
            'alt_text': 'Textiles premium pour hôtellerie de luxe',
            'width': 1200,
            'height': 800,
            'mime_type': 'image/jpeg',
            'file_size': 150000
        },
        {
            'file_name': 'medical-textile.jpg',
            'original_name': 'medical-textile.jpg',
            'alt_text': 'Linge médical de qualité',
            'width': 1200,
            'height': 800,
            'mime_type': 'image/jpeg',
            'file_size': 145000
        },
        {
            'file_name': 'literie.jpg',
            'original_name': 'literie.jpg',
            'alt_text': 'Literie de luxe confortable',
            'width': 1200,
            'height': 800,
            'mime_type': 'image/jpeg',
            'file_size': 155000
        }
    ]
    
    for img_data in blog_images:
        image = ImageAsset(**img_data)
        db.session.add(image)
    
    db.session.flush()  # Get the IDs for the images
    
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
        ('color_theme', 'silver', 'string', 'Thème de couleur du site (gold/silver)'),
        ('theme_mode', 'dark', 'string', 'Mode de thème par défaut (dark/light/auto)'),
        ('allow_user_theme_toggle', 'true', 'boolean', 'Permettre à l\'utilisateur de basculer le thème'),
    ]
    
    for key, value, setting_type, description in settings_data:
        setting = SiteSetting(
            key=key,
            value=value,
            setting_type=setting_type,
            description=description
        )
        db.session.add(setting)
    
    # Get image IDs for blog articles
    image_hotel = ImageAsset.query.filter_by(file_name='hotel-textile.jpg').first()
    image_medical = ImageAsset.query.filter_by(file_name='medical-textile.jpg').first()
    image_literie = ImageAsset.query.filter_by(file_name='literie.jpg').first()
    
    # Seed blog articles
    print("Seeding blog articles...")
    articles = [
        {
            'slug': 'innovation-textiles-premium',
            'title_fr': 'L\'Innovation dans les Textiles Premium pour l\'Hôtellerie',
            'title_en': 'Innovation in Premium Textiles for Hospitality',
            'excerpt_fr': 'Découvrez comment les dernières innovations en textile transforment l\'expérience hôtelière de luxe.',
            'excerpt_en': 'Discover how the latest textile innovations are transforming the luxury hotel experience.',
            'content_fr': '<p>L\'industrie hôtelière de luxe connaît une révolution grâce aux innovations dans le domaine des textiles premium. Chez KANSOTEX, nous sommes à la pointe de cette transformation.</p><h2>Les Nouvelles Technologies Textiles</h2><p>Les fibres intelligentes et les tissus durables redéfinissent le confort et l\'expérience client dans les hôtels 5 étoiles.</p><p>Nos textiles premium combinent durabilité exceptionnelle et confort suprême, offrant à vos clients une expérience inoubliable.</p>',
            'content_en': '<p>The luxury hospitality industry is experiencing a revolution thanks to innovations in premium textiles. At KANSOTEX, we are at the forefront of this transformation.</p><h2>New Textile Technologies</h2><p>Smart fibers and sustainable fabrics are redefining comfort and customer experience in 5-star hotels.</p><p>Our premium textiles combine exceptional durability and supreme comfort, offering your guests an unforgettable experience.</p>',
            'category_fr': 'Innovation',
            'category_en': 'Innovation',
            'tags_fr': 'hôtellerie,luxe,innovation,textiles',
            'tags_en': 'hospitality,luxury,innovation,textiles',
            'featured_image_id': image_hotel.id if image_hotel else None,
            'author_name': 'KANSOTEX Team',
            'meta_title_fr': 'Innovation Textiles Premium Hôtellerie | KANSOTEX',
            'meta_title_en': 'Premium Textile Innovation Hospitality | KANSOTEX',
            'meta_description_fr': 'Découvrez les innovations textiles qui transforment l\'hôtellerie de luxe.',
            'meta_description_en': 'Discover textile innovations transforming luxury hospitality.',
            'is_published': True,
            'published_at': datetime.utcnow()
        },
        {
            'slug': 'guide-choix-linge-medical',
            'title_fr': 'Guide Complet pour le Choix du Linge Médical de Qualité',
            'title_en': 'Complete Guide to Choosing Quality Medical Linen',
            'excerpt_fr': 'Tout ce que vous devez savoir pour choisir le linge médical adapté à votre établissement de santé.',
            'excerpt_en': 'Everything you need to know to choose the right medical linen for your healthcare facility.',
            'content_fr': '<p>Le choix du linge médical est crucial pour garantir l\'hygiène et le confort des patients.</p><h2>Normes et Certifications</h2><p>Les textiles médicaux doivent respecter des normes strictes de qualité et d\'hygiène.</p><h2>Durabilité et Résistance</h2><p>Notre linge médical est conçu pour résister aux lavages intensifs tout en maintenant sa douceur.</p>',
            'content_en': '<p>Choosing medical linen is crucial to ensure patient hygiene and comfort.</p><h2>Standards and Certifications</h2><p>Medical textiles must comply with strict quality and hygiene standards.</p><h2>Durability and Resistance</h2><p>Our medical linen is designed to withstand intensive washing while maintaining its softness.</p>',
            'category_fr': 'Médical',
            'category_en': 'Medical',
            'tags_fr': 'médical,santé,hygiène,qualité',
            'tags_en': 'medical,health,hygiene,quality',
            'featured_image_id': image_medical.id if image_medical else None,
            'author_name': 'KANSOTEX Team',
            'meta_title_fr': 'Guide Choix Linge Médical | KANSOTEX',
            'meta_title_en': 'Medical Linen Selection Guide | KANSOTEX',
            'meta_description_fr': 'Guide complet pour choisir le linge médical de qualité.',
            'meta_description_en': 'Complete guide to choosing quality medical linen.',
            'is_published': True,
            'published_at': datetime.utcnow()
        },
        {
            'slug': 'confort-literie-premium',
            'title_fr': 'Le Confort Ultime : Guide de la Literie Premium',
            'title_en': 'Ultimate Comfort: Premium Bedding Guide',
            'excerpt_fr': 'Découvrez comment choisir la literie premium parfaite pour transformer votre sommeil et celui de vos clients.',
            'excerpt_en': 'Discover how to choose the perfect premium bedding to transform your sleep and that of your guests.',
            'content_fr': '<p>La literie premium est bien plus qu\'un simple investissement - c\'est la clé d\'un sommeil réparateur et d\'une expérience client exceptionnelle.</p><h2>Qualité des Matériaux</h2><p>Les meilleurs tissus comme le coton égyptien et le lin européen offrent une durabilité incomparable et un confort absolu.</p><h2>Impact sur la Satisfaction Client</h2><p>Dans l\'hôtellerie, la qualité de la literie est directement liée à la satisfaction des clients et aux avis positifs.</p><h2>Nos Solutions KANSOTEX</h2><p>Nos collections de literie combinent excellence artisanale et innovation textile pour créer une expérience de sommeil unique.</p>',
            'content_en': '<p>Premium bedding is much more than a simple investment - it\'s the key to restorative sleep and an exceptional customer experience.</p><h2>Material Quality</h2><p>The finest fabrics like Egyptian cotton and European linen offer unparalleled durability and absolute comfort.</p><h2>Impact on Customer Satisfaction</h2><p>In hospitality, bedding quality is directly linked to guest satisfaction and positive reviews.</p><h2>Our KANSOTEX Solutions</h2><p>Our bedding collections combine artisan excellence and textile innovation to create a unique sleep experience.</p>',
            'category_fr': 'Literie',
            'category_en': 'Bedding',
            'tags_fr': 'literie,confort,luxe,sommeil,hôtellerie',
            'tags_en': 'bedding,comfort,luxury,sleep,hospitality',
            'featured_image_id': image_literie.id if image_literie else None,
            'author_name': 'KANSOTEX Team',
            'meta_title_fr': 'Guide Literie Premium | KANSOTEX',
            'meta_title_en': 'Premium Bedding Guide | KANSOTEX',
            'meta_description_fr': 'Découvrez nos conseils pour choisir la literie premium parfaite.',
            'meta_description_en': 'Discover our tips for choosing the perfect premium bedding.',
            'is_published': True,
            'published_at': datetime.utcnow()
        }
    ]
    
    for article_data in articles:
        article = BlogArticle(**article_data)
        db.session.add(article)
    
    # Seed testimonials
    print("Seeding testimonials...")
    testimonials_data = [
        {
            'client_name': 'Dr. Sophia Leroy',
            'client_title_fr': 'Chef de Service',
            'client_title_en': 'Head of Department',
            'client_company': 'Clinique SantéPlus',
            'content_fr': 'KANSOTEX a révolutionné le confort dans notre établissement médical. Leurs produits sont à la fois luxueux et pratiques, répondant parfaitement aux normes d\'hygiène strictes.',
            'content_en': 'KANSOTEX has revolutionized comfort in our medical facility. Their products are both luxurious and practical, perfectly meeting strict hygiene standards.',
            'rating': 5,
            'is_featured': True,
            'is_published': True,
            'display_order': 1
        },
        {
            'client_name': 'Julien Moreau',
            'client_title_fr': 'Directeur Général',
            'client_title_en': 'General Manager',
            'client_company': 'Hôtel Élégance',
            'content_fr': 'La qualité des textiles KANSOTEX a transformé l\'expérience de nos clients. Leur durabilité est impressionnante et le service est impeccable.',
            'content_en': 'The quality of KANSOTEX textiles has transformed our guests\' experience. Their durability is impressive and the service is impeccable.',
            'rating': 5,
            'is_featured': True,
            'is_published': True,
            'display_order': 2
        },
        {
            'client_name': 'Claire Dubois',
            'client_title_fr': 'Architecte d\'Intérieur',
            'client_title_en': 'Interior Designer',
            'client_company': 'Design & Espaces',
            'content_fr': 'En tant qu\'architecte d\'intérieur, je recommande KANSOTEX pour leur excellence et leur style unique. Un vrai partenaire de confiance pour tous mes projets haut de gamme.',
            'content_en': 'As an interior designer, I recommend KANSOTEX for their excellence and unique style. A true trusted partner for all my high-end projects.',
            'rating': 5,
            'is_featured': True,
            'is_published': True,
            'display_order': 3
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial = Testimonial(**testimonial_data)
        db.session.add(testimonial)
    
    db.session.commit()
    
    # Seed Collection Slides (only if none exist)
    if CollectionSlide.query.count() == 0:
        print("Seeding collection slides...")
        first_image = ImageAsset.query.first()
        image_id = first_image.id if first_image else None
        
        collection_slides_data = [
        {
            'title_fr': 'Textile Hôtelier Premium',
            'title_en': 'Premium Hotel Textiles',
            'description_fr': 'Draps, serviettes et linge de luxe pour hôtels 5 étoiles',
            'description_en': 'Sheets, towels and luxury linens for 5-star hotels',
            'button_text_fr': 'Découvrir',
            'button_text_en': 'Discover',
            'button_link': '#contact',
            'image_id': image_id,
            'display_order': 1,
            'is_visible': True
        },
        {
            'title_fr': 'Linge Médical Certifié',
            'title_en': 'Certified Medical Linens',
            'description_fr': 'Textiles conformes aux normes médicales les plus strictes',
            'description_en': 'Textiles compliant with the strictest medical standards',
            'button_text_fr': 'En savoir plus',
            'button_text_en': 'Learn more',
            'button_link': '#contact',
            'image_id': image_id,
            'display_order': 2,
            'is_visible': True
        },
        {
            'title_fr': 'Collection Maison',
            'title_en': 'Home Collection',
            'description_fr': 'Textiles de qualité supérieure pour votre domicile',
            'description_en': 'Superior quality textiles for your home',
            'button_text_fr': 'Explorer',
            'button_text_en': 'Explore',
            'button_link': '#contact',
            'image_id': image_id,
            'display_order': 3,
            'is_visible': True
        }
    ]
    
        for slide_data in collection_slides_data:
            slide = CollectionSlide(**slide_data)
            db.session.add(slide)
        db.session.commit()
        print("✓ Collection slides seeded!")
    
    # Seed Section Panels (only if none exist)
    if SectionPanel.query.count() == 0:
        print("Seeding section panels...")
        first_image = ImageAsset.query.first()
        image_id = first_image.id if first_image else None
        
        section_panels_data = [
        {
            'title_fr': 'Hôtellerie',
            'title_en': 'Hospitality',
            'subtitle_fr': 'Excellence Hôtelière',
            'subtitle_en': 'Hotel Excellence',
            'description_fr': 'Draps, serviettes et linge de maison haut de gamme pour hôtels et établissements de luxe',
            'description_en': 'High-end sheets, towels and linens for hotels and luxury establishments',
            'icon_class': 'fa-hotel',
            'button_text_fr': 'Découvrir',
            'button_text_en': 'Discover',
            'button_link': '#contact',
            'image_id': image_id,
            'background_color': '#1a1a2e',
            'display_order': 1,
            'is_visible': True
        },
        {
            'title_fr': 'Médical',
            'title_en': 'Medical',
            'subtitle_fr': 'Hygiène & Confort',
            'subtitle_en': 'Hygiene & Comfort',
            'description_fr': 'Linge médical certifié aux normes les plus strictes pour cliniques et hôpitaux',
            'description_en': 'Certified medical linens meeting the strictest standards for clinics and hospitals',
            'icon_class': 'fa-heartbeat',
            'button_text_fr': 'En savoir plus',
            'button_text_en': 'Learn more',
            'button_link': '#contact',
            'image_id': image_id,
            'background_color': '#2d3748',
            'display_order': 2,
            'is_visible': True
        },
        {
            'title_fr': 'Maison',
            'title_en': 'Home',
            'subtitle_fr': 'Confort & Élégance',
            'subtitle_en': 'Comfort & Elegance',
            'description_fr': 'Textiles premium pour sublimer votre intérieur avec style et confort',
            'description_en': 'Premium textiles to enhance your interior with style and comfort',
            'icon_class': 'fa-home',
            'button_text_fr': 'Explorer',
            'button_text_en': 'Explore',
            'button_link': '#contact',
            'image_id': image_id,
            'background_color': '#1a202c',
            'display_order': 3,
            'is_visible': True
        }
    ]
    
        for panel_data in section_panels_data:
            panel = SectionPanel(**panel_data)
            db.session.add(panel)
        db.session.commit()
        print("✓ Section panels seeded!")
    
    print("✓ Complete content seeded successfully!")
    print("✓ Blog articles and testimonials seeded!")

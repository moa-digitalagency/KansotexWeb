from main import create_app
from backend.models import db
from backend.models.content import ContentSection, ContentField, SiteSetting, SeoMeta

def seed_all_content():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding complete content structure...")
        
        sections_data = [
            {
                'slug': 'hero',
                'name': 'Section Héro',
                'description': 'Bannière principale de la page d\'accueil',
                'fields': {
                    'title': 'KANSOTEX',
                    'subtitle': 'Expert en Textiles de Qualité Premium',
                    'tagline': 'EXCELLENCE DEPUIS 2005',
                    'cta_text': 'Découvrir nos atouts',
                    'badge_1_icon': 'star',
                    'badge_1_text': '+20 ans d\'expertise',
                    'badge_2_icon': 'gem',
                    'badge_2_text': 'Qualité Premium',
                }
            },
            {
                'slug': 'forces',
                'name': 'Points Forts',
                'description': 'Section des points forts de l\'entreprise',
                'fields': {
                    'title': 'Nos Points Forts',
                    'description': 'Ce qui nous distingue dans l\'univers des textiles de qualité premium',
                    'strength_1_title': 'Expérience Significative',
                    'strength_1_text': 'Une expérience significative dans l\'accompagnement des professionnels désireux de se distinguer grâce à un travail de qualité alliant un choix méticuleux des tissus.',
                    'strength_2_title': 'Compréhension Parfaite',
                    'strength_2_text': 'Une parfaite compréhension des besoins des professionnels et des particuliers, ce qui nous permet de donner vie à vos projets.',
                    'strength_3_title': 'Personnalisation Expert',
                    'strength_3_text': 'Personnalisation de vos commandes en tenant compte de votre cahier de charge et des normes techniques grâce à notre atelier.',
                    'strength_4_title': 'Rapidité d\'Exécution',
                    'strength_4_text': 'Une rapidité dans l\'exécution des commandes pour répondre à vos besoins dans les meilleurs délais.',
                    'strength_5_title': 'Livraison Rapide',
                    'strength_5_text': 'Livraison partout au Maroc dans un délai de 24h pour assurer votre satisfaction.',
                    'strength_6_title': '+20 Ans d\'Excellence',
                    'strength_6_text': 'Expert reconnu dans les textiles premium pour hôtels, cliniques et maisons. Une expérience de luxe inégalée.',
                }
            },
            {
                'slug': 'collection',
                'name': 'Notre Collection',
                'description': 'Section collection de produits - 6 slides carousel',
                'fields': {
                    'title': 'Notre Collection Premium',
                    'description': 'Découvrez l\'excellence de nos textiles de luxe',
                    'slide_1_category': 'HÔTELLERIE DE LUXE',
                    'slide_1_title': 'Literie Hôtelière',
                    'slide_1_description': 'Confort exceptionnel et élégance raffinée',
                    'slide_2_category': 'SECTEUR MÉDICAL',
                    'slide_2_title': 'Textiles Médicaux',
                    'slide_2_description': 'Hygiène et qualité professionnelle',
                    'slide_3_category': 'RÉSIDENTIEL',
                    'slide_3_title': 'Linge de Maison',
                    'slide_3_description': 'Douceur et raffinement pour votre intérieur',
                    'slide_4_category': 'HAUTE GASTRONOMIE',
                    'slide_4_title': 'Textiles Restaurant',
                    'slide_4_description': 'Élégance pour tables d\'exception',
                    'slide_5_category': 'SPA & WELLNESS',
                    'slide_5_title': 'Linge de Spa',
                    'slide_5_description': 'Bien-être et luxe absolu',
                    'slide_6_category': 'ÉVÉNEMENTIEL',
                    'slide_6_title': 'Textiles Événementiels',
                    'slide_6_description': 'Prestance pour vos événements',
                }
            },
            {
                'slug': 'volets',
                'name': 'Nos Volets',
                'description': 'Nos différents secteurs d\'activité - 4 volets',
                'fields': {
                    'title': 'Les Volets Que Nous Servons',
                    'description': 'Solutions textiles adaptées à tous vos besoins professionnels et personnels',
                    'volet_1_title': 'Home Textile',
                    'volet_1_description': 'Linge de maison haut de gamme pour un confort quotidien inégalé et une décoration raffinée.',
                    'volet_2_title': 'Hotel Textile',
                    'volet_2_description': 'Solutions premium pour l\'hôtellerie de luxe et les établissements haut de gamme.',
                    'volet_3_title': 'Medical Textile',
                    'volet_3_description': 'Textiles médicaux professionnels répondant aux normes d\'hygiène les plus strictes.',
                    'volet_4_title': 'Residential Textile',
                    'volet_4_description': 'Solutions complètes pour résidences privées et projets immobiliers de prestige.',
                }
            },
            {
                'slug': 'engagement',
                'name': 'Notre Engagement',
                'description': 'Nos engagements qualité - 3 piliers',
                'fields': {
                    'title': 'Notre Engagement',
                    'pillar_1_title': 'Qualité Premium',
                    'pillar_1_text': 'Chez Kansotex, nous sélectionnons uniquement des tissus de première qualité, garantissant durabilité et confort exceptionnels.',
                    'pillar_2_title': 'Service Client',
                    'pillar_2_text': 'Chaque produit passe par un processus de contrôle rigoureux pour assurer une finition parfaite et une satisfaction client maximale.',
                    'pillar_3_title': 'Innovation',
                    'pillar_3_text': 'Nous nous engageons à une innovation constante afin de vous offrir constamment des produits tendance et au summum du confort.',
                }
            },
            {
                'slug': 'testimonials',
                'name': 'Témoignages',
                'description': 'Témoignages clients - 3 témoignages',
                'fields': {
                    'title': 'Témoignages Clients',
                    'description': 'Ce que nos clients disent de nous',
                    'testimonial_1_text': 'Excellente qualité et service impeccable. KANSOTEX a transformé notre établissement avec des textiles d\'une qualité exceptionnelle.',
                    'testimonial_1_author': 'Hôtel Royal Palace',
                    'testimonial_1_role': 'Directeur Général',
                    'testimonial_2_text': 'Un partenaire de confiance depuis des années. La qualité des produits et le respect des délais sont exemplaires.',
                    'testimonial_2_author': 'Clinique Atlas',
                    'testimonial_2_role': 'Responsable Achats',
                    'testimonial_3_text': 'Des textiles de luxe qui allient confort et élégance. Notre clientèle apprécie énormément la qualité du linge.',
                    'testimonial_3_author': 'Restaurant Le Gourmet',
                    'testimonial_3_role': 'Chef Propriétaire',
                }
            },
            {
                'slug': 'footer',
                'name': 'Footer',
                'description': 'Pied de page du site',
                'fields': {
                    'company_name': 'KANSOTEX',
                    'company_description': 'Expert en textiles de qualité premium depuis plus de 20 ans. Nous vous accompagnons dans vos projets hôteliers, médicaux et résidentiels avec passion et excellence.',
                    'menu_1_title': 'Navigation',
                    'menu_2_title': 'Services',
                    'menu_3_title': 'Contact',
                    'contact_address': 'Casablanca, Maroc',
                    'contact_phone': '+212 5XX XX XX XX',
                    'contact_email': 'contact@kansotex.ma',
                    'social_facebook': 'https://facebook.com/kansotex',
                    'social_instagram': 'https://instagram.com/kansotex',
                    'social_linkedin': 'https://linkedin.com/company/kansotex',
                    'copyright': '© 2025 KANSOTEX. Tous droits réservés.',
                }
            },
            {
                'slug': 'contact',
                'name': 'Contact',
                'description': 'Section formulaire de contact',
                'fields': {
                    'title': 'Contactez-Nous',
                    'description': 'Besoin de renseignements ou d\'un devis ? Notre équipe est à votre écoute',
                    'form_name_placeholder': 'Votre nom',
                    'form_email_placeholder': 'Votre email',
                    'form_phone_placeholder': 'Votre téléphone',
                    'form_message_placeholder': 'Votre message',
                    'form_submit_text': 'Envoyer',
                }
            }
        ]
        
        for section_data in sections_data:
            section = ContentSection.query.filter_by(slug=section_data['slug']).first()
            
            if not section:
                section = ContentSection(
                    slug=section_data['slug'],
                    name=section_data['name'],
                    description=section_data.get('description')
                )
                db.session.add(section)
                db.session.flush()
                print(f"✓ Created section: {section_data['name']}")
            else:
                print(f"- Section exists: {section_data['name']}")
            
            for key, value in section_data['fields'].items():
                field = ContentField.query.filter_by(section_id=section.id, key=key).first()
                if not field:
                    field = ContentField(
                        section_id=section.id,
                        key=key,
                        value=value,
                        field_type='text',
                        order=list(section_data['fields'].keys()).index(key)
                    )
                    db.session.add(field)
                    print(f"  + Added field: {key}")
        
        print("\n🌐 Seeding site settings...")
        site_settings = [
            {'key': 'site_name', 'value': 'KANSOTEX', 'setting_type': 'string', 'description': 'Nom du site'},
            {'key': 'site_tagline', 'value': 'Expert en Textiles de Qualité Premium', 'setting_type': 'string', 'description': 'Slogan du site'},
            {'key': 'contact_email', 'value': 'contact@kansotex.ma', 'setting_type': 'string', 'description': 'Email de contact'},
            {'key': 'contact_phone', 'value': '+212 5XX XX XX XX', 'setting_type': 'string', 'description': 'Téléphone de contact'},
            {'key': 'contact_address', 'value': 'Casablanca, Maroc', 'setting_type': 'string', 'description': 'Adresse'},
            {'key': 'facebook_url', 'value': 'https://facebook.com/kansotex', 'setting_type': 'url', 'description': 'URL Facebook'},
            {'key': 'instagram_url', 'value': 'https://instagram.com/kansotex', 'setting_type': 'url', 'description': 'URL Instagram'},
            {'key': 'linkedin_url', 'value': 'https://linkedin.com/company/kansotex', 'setting_type': 'url', 'description': 'URL LinkedIn'},
            {'key': 'default_meta_title', 'value': 'KANSOTEX - Expert en Textiles de Qualité Premium', 'setting_type': 'string', 'description': 'Titre SEO par défaut'},
            {'key': 'default_meta_description', 'value': 'KANSOTEX, expert en textiles premium pour hôtellerie, secteur médical et résidentiel depuis plus de 20 ans. Qualité, innovation et service d\'excellence.', 'setting_type': 'text', 'description': 'Description SEO par défaut'},
            {'key': 'default_meta_keywords', 'value': 'textiles premium, linge hôtelier, textiles médicaux, linge de maison, Maroc, Casablanca, qualité, luxe', 'setting_type': 'text', 'description': 'Mots-clés SEO par défaut'},
        ]
        
        for setting_data in site_settings:
            setting = SiteSetting.query.filter_by(key=setting_data['key']).first()
            if not setting:
                setting = SiteSetting(**setting_data)
                db.session.add(setting)
                print(f"✓ Added setting: {setting_data['key']}")
            else:
                print(f"- Setting exists: {setting_data['key']}")
        
        print("\n🔍 Seeding SEO metadata...")
        seo_data = [
            {
                'page_slug': 'home',
                'meta_title': 'KANSOTEX - Expert en Textiles de Qualité Premium | Maroc',
                'meta_description': 'KANSOTEX, leader des textiles premium au Maroc. Solutions hôtelières, médicales et résidentielles. +20 ans d\'excellence. Qualité et innovation garanties.',
                'meta_keywords': 'textiles premium maroc, linge hôtelier casablanca, textiles médicaux, linge de maison luxe, kansotex',
                'og_title': 'KANSOTEX - Expert Textiles Premium Maroc',
                'og_description': 'Textiles de luxe pour hôtels, cliniques et résidences. +20 ans d\'expertise au Maroc.',
                'twitter_card': 'summary_large_image',
            }
        ]
        
        for seo in seo_data:
            seo_meta = SeoMeta.query.filter_by(page_slug=seo['page_slug']).first()
            if not seo_meta:
                seo_meta = SeoMeta(**seo)
                db.session.add(seo_meta)
                print(f"✓ Added SEO meta for: {seo['page_slug']}")
            else:
                print(f"- SEO meta exists for: {seo['page_slug']}")
        
        db.session.commit()
        print("\n✅ Complete content seeding finished successfully!")

if __name__ == '__main__':
    seed_all_content()

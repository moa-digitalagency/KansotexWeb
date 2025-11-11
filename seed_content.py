from main import create_app
from backend.models import db
from backend.models.content import ContentSection, ContentField

def seed_content():
    app = create_app()
    with app.app_context():
        print("Seeding content sections...")
        
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
                'slug': 'engagement',
                'name': 'Notre Engagement',
                'description': 'Nos engagements qualité',
                'fields': {
                    'title': 'Notre Engagement',
                    'description': 'Des valeurs fortes au service de votre satisfaction',
                    'engagement_1_title': 'Matériaux Haut de Gamme',
                    'engagement_1_text': 'Chez Kansotex, nous sélectionnons uniquement des tissus de première qualité, garantissant durabilité et confort exceptionnels.',
                    'engagement_2_title': 'Contrôle de Qualité Rigoureux',
                    'engagement_2_text': 'Chaque produit passe par un processus de contrôle rigoureux pour assurer une finition parfaite et une satisfaction client maximale.',
                    'engagement_3_title': 'Innovation Constante',
                    'engagement_3_text': 'Nous nous engageons à une innovation constante afin de vous offrir constamment des produits tendance et au summum du confort.',
                }
            },
            {
                'slug': 'collection',
                'name': 'Notre Collection',
                'description': 'Section collection de produits',
                'fields': {
                    'title': 'Notre Collection Premium',
                    'description': 'Découvrez l\'excellence de nos textiles de luxe',
                }
            },
            {
                'slug': 'volets',
                'name': 'Nos Volets',
                'description': 'Nos différents secteurs d\'activité',
                'fields': {
                    'title': 'Nos Volets d\'Excellence',
                    'description': 'Des solutions textiles adaptées à chaque secteur',
                }
            },
            {
                'slug': 'contact',
                'name': 'Contact',
                'description': 'Informations de contact',
                'fields': {
                    'title': 'Infos Contact',
                    'description': 'Contactez-nous pour tous vos besoins en textiles premium',
                    'company_name': 'KANSOTEX',
                    'company_description': 'Expert en textiles de qualité premium, nous vous accompagnons depuis plus de 20 ans dans vos projets hôteliers, médicaux et résidentiels.',
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
                
                for key, value in section_data['fields'].items():
                    field = ContentField(
                        section_id=section.id,
                        key=key,
                        value=value,
                        field_type='text',
                        order=list(section_data['fields'].keys()).index(key)
                    )
                    db.session.add(field)
                
                print(f"✓ Created section: {section_data['name']}")
            else:
                print(f"- Section already exists: {section_data['name']}")
        
        db.session.commit()
        print("\n✓ Content seeding completed successfully!")

if __name__ == '__main__':
    seed_content()

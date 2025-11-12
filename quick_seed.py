from main import create_app
from backend.models import db
from backend.models.content import ContentSection, ContentField

app = create_app()
with app.app_context():
    print("Quick seeding...")
    
    sections = [
        ('forces', 'Points Forts', [
            ('title', 'Nos Points Forts'),
            ('description', 'Ce qui nous distingue dans l\'univers des textiles de qualité premium'),
        ]),
        ('collection', 'Collection', [
            ('title', 'Notre Collection Premium'),
            ('description', 'Découvrez l\'excellence de nos textiles de luxe'),
        ]),
        ('volets', 'Volets', [
            ('title', 'Nos Volets d\'Excellence'),
            ('description', 'Des solutions textiles adaptées à chaque secteur'),
        ]),
        ('engagement', 'Engagement', [
            ('title', 'Notre Engagement'),
            ('description', 'Des valeurs fortes au service de votre satisfaction'),
        ]),
        ('contact', 'Contact', [
            ('title', 'Contactez-Nous'),
            ('address', 'Casablanca, Maroc'),
            ('phone', '+212 5XX-XXXXXX'),
            ('email', 'contact@kansotex.ma'),
        ]),
    ]
    
    for slug, name, fields in sections:
        section = ContentSection.query.filter_by(slug=slug).first()
        if not section:
            section = ContentSection(slug=slug, name=name)
            db.session.add(section)
            db.session.flush()
            print(f'Created section: {slug}')
        
        for key, value in fields:
            field = ContentField.query.filter_by(section_id=section.id, key=key).first()
            if not field:
                field = ContentField(
                    section_id=section.id,
                    key=key,
                    value=value,
                    field_type='text'
                )
                db.session.add(field)
    
    db.session.commit()
    print("Quick seed complete!")

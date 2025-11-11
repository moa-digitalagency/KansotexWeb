from backend.models import db
from backend.models.contact import Contact

class ContactService:
    def create_contact(self, name, email, phone, message):
        contact = Contact(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        db.session.add(contact)
        db.session.commit()
        return contact
    
    def get_all_contacts(self):
        return Contact.query.order_by(Contact.created_at.desc()).all()
    
    def get_contact_by_id(self, contact_id):
        return Contact.query.get(contact_id)

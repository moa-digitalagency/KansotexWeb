from backend.models import db
from backend.models.contact import Contact
from backend.models.content import SiteSetting
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

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
        
        self.send_contact_email(name, email, phone, message)
        
        return contact
    
    def send_contact_email(self, name, email, phone, message):
        try:
            recipient_email = SiteSetting.get_setting('contact_recipient_email')
            smtp_host = SiteSetting.get_setting('smtp_host')
            smtp_port_str = SiteSetting.get_setting('smtp_port', '587')
            smtp_use_tls = SiteSetting.get_setting('smtp_use_tls', 'true')
            sender_email = SiteSetting.get_setting('smtp_sender_email')
            
            smtp_username = os.environ.get('SMTP_USERNAME')
            smtp_password = os.environ.get('SMTP_PASSWORD')
            
            if not all([recipient_email, smtp_host, smtp_username, smtp_password, sender_email]):
                print("Configuration SMTP incomplète. Email non envoyé.")
                print(f"  - recipient_email: {'OK' if recipient_email else 'MANQUANT'}")
                print(f"  - smtp_host: {'OK' if smtp_host else 'MANQUANT'}")
                print(f"  - smtp_username: {'OK' if smtp_username else 'MANQUANT'}")
                print(f"  - smtp_password: {'OK' if smtp_password else 'MANQUANT'}")
                print(f"  - sender_email: {'OK' if sender_email else 'MANQUANT'}")
                return False
            
            try:
                smtp_port = int(smtp_port_str)
                if smtp_port < 1 or smtp_port > 65535:
                    print(f"Port SMTP invalide: {smtp_port}. Utilisation du port 587.")
                    smtp_port = 587
            except (ValueError, TypeError):
                print(f"Port SMTP non numérique: {smtp_port_str}. Utilisation du port 587.")
                smtp_port = 587
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Nouveau message de contact de {name}"
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Reply-To'] = email
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                        <h2 style="color: #D4AF37; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">
                            Nouveau message de contact
                        </h2>
                        <div style="margin: 20px 0;">
                            <p><strong>Nom :</strong> {name}</p>
                            <p><strong>Email :</strong> <a href="mailto:{email}">{email}</a></p>
                            <p><strong>Téléphone :</strong> {phone if phone else 'Non fourni'}</p>
                        </div>
                        <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #D4AF37; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #555;">Message :</h3>
                            <p style="white-space: pre-wrap;">{message}</p>
                        </div>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="color: #888; font-size: 12px;">
                            Ce message a été envoyé depuis le formulaire de contact de votre site web.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            text_body = f"""
            Nouveau message de contact
            
            Nom: {name}
            Email: {email}
            Téléphone: {phone if phone else 'Non fourni'}
            
            Message:
            {message}
            
            ---
            Ce message a été envoyé depuis le formulaire de contact de votre site web.
            """
            
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            server = smtplib.SMTP(smtp_host, int(smtp_port))
            if smtp_use_tls == 'true':
                server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email envoyé avec succès à {recipient_email}")
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {str(e)}")
            return False
    
    def get_all_contacts(self):
        return Contact.query.order_by(Contact.created_at.desc()).all()
    
    def get_contact_by_id(self, contact_id):
        return Contact.query.get(contact_id)

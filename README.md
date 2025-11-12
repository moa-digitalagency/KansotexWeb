# KANSOTEX - Expert en Textiles de Qualité Premium

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-3.0.0-green)
![License](https://img.shields.io/badge/license-Proprietary-red)

Site web premium pour KANSOTEX, expert en textiles de qualité premium avec **+20 ans d'expertise** au Maroc.

## 📋 Table des Matières

- [À Propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Déploiement](#déploiement)
- [Structure du Projet](#structure-du-projet)
- [Panneau d'Administration](#panneau-dadministration)
- [Système de Thèmes](#système-de-thèmes)

## 🎯 À Propos

KANSOTEX est une entreprise marocaine spécialisée dans les textiles de qualité premium pour :
- 🏨 **Hôtellerie de luxe** - Literie et linge haut de gamme
- 🏥 **Secteur médical** - Textiles conformes aux normes strictes
- 🏠 **Résidentiel** - Solutions élégantes pour la maison

### Notre Engagement
Fournir une expérience de luxe inégalée avec des tissus de première qualité, un contrôle rigoureux et une innovation constante.

## ✨ Fonctionnalités

### Site Public
- 🎨 **Système de thèmes dual** : Gold (or) et Silver (argent)
- 🖼️ **Hero slider** automatique avec 3 images en rotation
- 📱 **Design responsive** adapté mobile, tablette, desktop
- 🎯 **Section Points Forts** avec 6 atouts clés
- 🛍️ **Carousel Collection Premium** (6 slides, auto-play 5s)
- 🎭 **Carousel Témoignages** clients interactif
- 📝 **Formulaire de contact** avec stockage en base de données
- 🎨 **Animations fluides** avec transitions CSS
- 🔍 **Navigation sticky** avec effet de flou dynamique

### Panneau d'Administration (`/admin/login`)
- 🔐 **Authentification sécurisée** par mot de passe
- ✏️ **Éditeur de contenu** pour toutes les sections du site
- 🖼️ **Gestion d'images** avec upload et preview
- 🎨 **Sélecteur de thème** (Gold ↔ Silver)
- 📊 **Gestion des témoignages** clients
- 📧 **Visualisation des messages** de contact
- ⚙️ **Configuration SEO** (meta tags, description)

## 🛠️ Technologies

### Backend
- **Python 3.11** - Langage principal
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM pour base de données
- **PostgreSQL** - Base de données relationnelle
- **Gunicorn** - Serveur WSGI pour production
- **Flask-WTF** - Formulaires avec protection CSRF
- **Pillow** - Traitement d'images

### Frontend
- **HTML5** - Structure sémantique
- **Tailwind CSS** - Framework CSS utility-first
- **JavaScript Vanilla** - Interactivité (sliders, navigation)
- **Font Awesome** - Icônes
- **Google Fonts** - Typographie (Inter)

### Sécurité & Performance
- Protection CSRF sur tous les formulaires
- Sessions sécurisées avec secret key
- Validation des uploads d'images
- Pool de connexions PostgreSQL optimisé
- Cache-Control pour éviter le cache navigateur

## 🚀 Installation

### Prérequis
- Python 3.11+
- PostgreSQL 12+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <repository-url>
cd kansotex
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement**

Créer un fichier `.env` à la racine :
```env
DATABASE_URL=postgresql://user:password@localhost:5432/kansotex
SESSION_SECRET=votre-secret-key-tres-longue-et-securisee
ADMIN_PASSWORD=votre_mot_de_passe_admin
```

4. **Initialiser la base de données**

La base de données est automatiquement créée et seedée au premier lancement :
```bash
python main.py
```

Le script crée les tables et charge le contenu initial automatiquement.

## ⚙️ Configuration

### Variables d'Environnement

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `DATABASE_URL` | URL de connexion PostgreSQL | ✅ |
| `SESSION_SECRET` | Clé secrète pour les sessions | ✅ |
| `ADMIN_PASSWORD` | Mot de passe du panneau admin | ✅ |

### Configuration de l'Application

Le fichier `config.py` contient la configuration Flask :
- Pool de connexions PostgreSQL (recyclage toutes les 300s)
- Protection CSRF activée
- Durée de session : 8 heures
- Limite d'upload : 10 MB

## 🌐 Déploiement

### Développement

```bash
python main.py
```
Serveur de développement sur `http://0.0.0.0:5000`

### Production (Replit)

Le déploiement est configuré avec **Gunicorn** :
```bash
gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=2 main:app
```

**Configuration automatique** :
- 2 workers Gunicorn
- Reuse-port activé pour zero-downtime
- Autoscale deployment pour économie de ressources

### Variables à configurer en Production
1. `DATABASE_URL` - URL de la base PostgreSQL de production
2. `SESSION_SECRET` - Clé secrète forte (générer avec `python -c "import secrets; print(secrets.token_hex(32))"`)
3. `ADMIN_PASSWORD` - Mot de passe admin sécurisé

## 📁 Structure du Projet

```
kansotex/
├── backend/
│   ├── models/              # Modèles SQLAlchemy
│   │   ├── content.py       # ContentSection, ContentField
│   │   ├── testimonial.py   # Testimonials
│   │   ├── contact.py       # Messages de contact
│   │   └── settings.py      # Paramètres site (thème, SEO)
│   ├── routes/
│   │   └── main.py          # Routes publiques (/, /contact)
│   ├── services/
│   │   └── content_provider.py  # Service de récupération contenu
│   ├── admin/
│   │   ├── routes.py        # Routes admin (/admin/*)
│   │   ├── forms.py         # Formulaires WTForms
│   │   └── services/        # Services admin (contenu, images)
│   ├── utils/
│   │   └── image_handler.py # Gestion des uploads d'images
│   └── seed_data.py         # Script d'initialisation DB
├── templates/
│   ├── index.html           # Page d'accueil publique
│   └── admin/               # Templates du panneau admin
│       ├── login.html
│       ├── dashboard.html
│       ├── edit_content.html
│       ├── manage_images.html
│       └── settings.html
├── static/
│   ├── css/
│   │   └── style.css        # Styles personnalisés + variables CSS
│   ├── js/
│   │   └── main.js          # JavaScript (sliders, navigation)
│   ├── images/              # Images du site par défaut
│   └── uploads/             # Images uploadées via admin
├── config.py                # Configuration Flask
├── main.py                  # Point d'entrée de l'application
├── requirements.txt         # Dépendances Python
├── .env                     # Variables d'environnement (git ignored)
└── README.md                # Ce fichier
```

## 🔐 Panneau d'Administration

### Accès
- **URL** : `/admin/login`
- **Mot de passe** : Défini dans la variable d'environnement `ADMIN_PASSWORD`

### Fonctionnalités Admin

#### 1. Gestion de Contenu (`/admin/content`)
- Éditer toutes les sections : Hero, Points Forts, Collection, Volets, Engagement, Contact
- Types de champs : Texte, Textarea, Image
- Sauvegarde instantanée avec feedback visuel

#### 2. Gestion d'Images (`/admin/images`)
- Upload d'images (max 10 MB)
- Preview instantané
- Liste de toutes les images uploadées
- Copie du chemin pour utilisation

#### 3. Témoignages (`/admin/testimonials`)
- Ajouter/modifier/supprimer des témoignages clients
- Champs : Nom, entreprise, texte, note (1-5 étoiles)

#### 4. Paramètres (`/admin/settings`)
- **Sélecteur de thème** : Gold (or) / Silver (argent)
- **Configuration SEO** : Meta title, description, keywords
- Changements appliqués en temps réel

## 🎨 Système de Thèmes

Le site propose deux thèmes dynamiques basés sur des **variables CSS** :

### Thème Gold (Or) 🌟
```css
--accent-light: #B8941E
--accent-mid: #D4AF37
--accent-dark: #9A7B15
--accent-rgb: 184, 148, 30
```

### Thème Silver (Argent) ✨
```css
--accent-light: #E8E8E8
--accent-mid: #C0C0C0
--accent-dark: #A8A8A8
--accent-rgb: 232, 232, 232
```

**Tous les éléments** s'adaptent automatiquement :
- Boutons et CTA
- Bordures et accents
- Icônes et badges
- Dégradés et ombres
- Numéros dans la section Engagement

## 🗄️ Base de Données

### Modèles Principaux

#### ContentSection
Sections de contenu du site (Hero, Forces, Collection, etc.)

#### ContentField
Champs de contenu (texte, image) associés aux sections

#### Testimonial
Témoignages clients avec nom, entreprise, texte, note

#### ContactMessage
Messages reçus via le formulaire de contact

#### SiteSettings
Paramètres globaux : thème actif, SEO, configuration

### Initialisation Automatique
Au premier lancement, la base est automatiquement :
1. Créée avec toutes les tables
2. Seedée avec le contenu par défaut
3. Configurée avec le thème Gold

## 📞 Informations de Contact

- **ICE** : 002323065B06
- **Téléphone** : +212 50 898 989
- **Email** : contact@kansotex.com
- **Localisation** : Maroc

## 📝 License

© 2025 KANSOTEX. Tous droits réservés.

---

**Expert en textiles de qualité premium depuis plus de 20 ans.**

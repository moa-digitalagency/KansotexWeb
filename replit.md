# KANSOTEX - Site Web

## Vue d'ensemble
Site web pour KANSOTEX, expert en textiles de qualité premium. Le site présente les services, produits et expertise de l'entreprise dans les secteurs hôtelier, médical et résidentiel.

## Stack Technique
- **Backend**: Python 3.11 + Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Vanilla)
- **Base de données**: PostgreSQL
- **Architecture**: Structure MVC avec backend organisé (routes, models, services, utils)

## Structure du Projet
```
/backend
  /routes - Routes Flask (API et pages)
  /models - Modèles de base de données SQLAlchemy
  /services - Logique métier et fournisseurs de contenu
  /admin - Panneau d'administration
    /services - Services admin (gestion contenu et images)
    routes.py - Routes admin
    forms.py - Formulaires admin
  /utils - Utilitaires
/templates - Templates HTML (Jinja2)
  /admin - Templates du panneau admin
/static
  /css - Styles personnalisés
  /js - JavaScript pour interactivité
  /images - Images du site (incluant images de collection et arrière-plans)
  /uploads - Images téléchargées via l'admin
config.py - Configuration de l'application (racine)
main.py - Point d'entrée de l'application Flask
seed_content.py - Script d'initialisation du contenu
```

## Fonctionnalités

### Site Public
- **Système de thème dark/light dynamique** avec bouton de changement
- **Détection automatique de la langue** du navigateur (FR/EN)
- Hero section avec slider d'images automatique (3 images)
- Header transparent qui devient opaque en mode sticky avec effet de flou
- Section "Nos Points Forts" avec les 6 atouts clés de KANSOTEX
- **Carousel de collection premium** (6 slides, auto-play 5s) - Positionné haut après Points Forts
  - Design premium avec badges de catégorie sur fond semi-transparent
  - Titres impactants text-5xl/6xl avec descriptions enrichies
  - Icônes de caractéristiques pour chaque slide
  - Boutons de navigation XL avec dégradés et effets hover
  - Images avec effet zoom subtil (scale-105), hauteur 600px
  - Navigation par dots et flèches prev/next
- Section "Les volets que nous servons" avec images d'arrière-plan subtiles
- **Section "Notre engagement" responsive** - 3 colonnes sur desktop, 1 colonne sur mobile/tablette
  - Contenu dynamique chargé depuis la base de données
  - Images d'arrière-plan subtiles (3 piliers)
- Carousel de témoignages clients interactif
- Formulaire de contact fonctionnel avec:
  - Stockage en base de données
  - **Envoi d'emails automatique via SMTP** aux administrateurs
  - Emails HTML formatés avec toutes les informations du contact
  - Gestion robuste des erreurs avec logs détaillés
- **Footer modernisé** avec layout 4 colonnes, icônes sociales, ligne de dégradé doré
- Design responsive en thème noir et or foncé (#B8941E) premium
- Animations et transitions fluides
- Navigation responsive avec menu mobile

### Panneau d'Administration
- **Accès sécurisé** via `/admin` avec authentification par mot de passe
- **Gestion de contenu** - Édition de tous les textes du site par section
- **Gestion des images** - Téléchargement, visualisation et suppression d'images
- **Upload d'images** avec optimisation automatique (Pillow)
  - Support JPG, PNG, GIF, WEBP
  - Compression et optimisation automatique (qualité 85%)
  - Conversion automatique en RGB
  - Limite de taille: 10 MB
- **Cropping d'images** - Recadrage des images selon les formats requis
- **Système de thème & apparence**
  - Mode de thème par défaut (dark/light)
  - Autorisation pour les visiteurs de changer le thème via bouton flottant
  - Sauvegarde de la préférence dans localStorage
- **Langue & Localisation**
  - Détection automatique de la langue du navigateur (FR/EN)
  - Paramètre activable/désactivable dans les settings
- **Configuration Email/SMTP** - Paramètres d'envoi d'emails pour le formulaire de contact
  - Email destinataire pour les messages de contact
  - Serveur SMTP (host, port, TLS)
  - Email expéditeur
  - Validation automatique du port SMTP (1-65535, défaut 587)
  - Avertissements si la configuration est incomplète
  - Credentials SMTP stockés de manière sécurisée dans les Secrets
- **Tableau de bord** avec statistiques et accès rapide
- **Sessions sécurisées** avec expiration automatique (8 heures)
- **Interface responsive** adaptée aux écrans desktop et mobile

## Base de Données

### Modèle Contact
- id (Integer, clé primaire)
- name (String 100, requis)
- email (String 120, requis)
- phone (String 20, optionnel)
- message (Text, requis)
- created_at (DateTime, auto)

### Modèles CMS (Content Management System)

#### ContentSection
- id (Integer, clé primaire)
- slug (String 100, unique)
- name (String 200)
- description (Text)
- created_at, updated_at (DateTime)

#### ContentField
- id (Integer, clé primaire)
- section_id (FK vers ContentSection)
- key (String 100)
- value (Text)
- field_type (String 50) - 'text' ou 'image'
- order (Integer)
- image_id (FK vers ImageAsset, optionnel)
- created_at, updated_at (DateTime)

#### ImageAsset
- id (Integer, clé primaire)
- file_name (String 255, unique)
- original_name (String 255)
- alt_text (String 255)
- width, height (Integer)
- mime_type (String 50)
- file_size (Integer)
- uploaded_at (DateTime)

#### SiteSetting
- id (Integer, clé primaire)
- key (String 100, unique)
- value (Text)
- setting_type (String 50)
- description (Text)
- updated_at (DateTime)

#### AdminSession
- id (Integer, clé primaire)
- session_token (String 255, unique)
- ip_address (String 50)
- user_agent (String 255)
- created_at, expires_at, last_activity (DateTime)

## Configuration
Le serveur Flask écoute sur `0.0.0.0:5000` pour permettre l'accès via le proxy Replit.

## Variables d'Environnement
- **DATABASE_URL** - URL de connexion PostgreSQL (requis)
- **SESSION_SECRET** - Clé secrète pour les sessions Flask (requis)
- **ADMIN_PASSWORD** - Mot de passe du panneau d'administration (requis)
- **SMTP_USERNAME** - Nom d'utilisateur SMTP pour l'envoi d'emails (optionnel, requis si SMTP configuré)
- **SMTP_PASSWORD** - Mot de passe SMTP pour l'envoi d'emails (optionnel, requis si SMTP configuré)

## Accès au Panneau d'Administration
1. Accéder à `/admin/login`
2. Entrer le mot de passe (ADMIN_PASSWORD)
3. Gérer le contenu via le tableau de bord

## Démarrage
L'application démarre automatiquement via le workflow configuré qui exécute `python main.py`.

## Contenu Dynamique (CMS)

Toutes les sections suivantes sont maintenant **complètement dynamiques** et éditables via le panneau d'administration:

### Section Hero (slug: 'hero')
- `title` - Titre principal "KANSOTEX"
- `subtitle` - Sous-titre "Expert en Textiles de Qualité Premium"
- `tagline` - Badge "EXCELLENCE DEPUIS 2005"
- `cta_text` - Texte du bouton d'action

### Section Points Forts (slug: 'forces')
- `title` - Titre de la section
- `description` - Description de la section
- `strength_1_title` / `strength_1_text` - Carte 1: Expérience Significative
- `strength_2_title` / `strength_2_text` - Carte 2: Compréhension Parfaite
- `strength_3_title` / `strength_3_text` - Carte 3: Personnalisation Expert
- `strength_4_title` / `strength_4_text` - Carte 4: Rapidité d'Exécution
- `strength_5_title` / `strength_5_text` - Carte 5: Livraison Rapide
- `strength_6_title` / `strength_6_text` - Carte 6: +20 Ans d'Excellence

### Section Collection (slug: 'collection')
- `title` - Titre de la section
- `description` - Description de la section

### Section Volets (slug: 'volets')
- `title` - Titre de la section
- `description` - Description de la section

### Section Engagement (slug: 'engagement')
- `title` - Titre de la section
- `pillar_1_title` / `pillar_1_text` - Pilier 1: Qualité Premium
- `pillar_2_title` / `pillar_2_text` - Pilier 2: Service Client
- `pillar_3_title` / `pillar_3_text` - Pilier 3: Innovation

### Section Contact (slug: 'contact')
- `title` - Titre de la section
- `description` - Description de la section

**Pattern d'utilisation dans les templates:**
```jinja2
{{ content.section_slug.field_key.value if content.section_slug and content.section_slug.field_key else 'Fallback Text' }}
```

## Dernières Modifications
- **2025-11-12: Système de thème dark/light dynamique**
  - Ajout de paramètres dans `/admin/settings` pour configurer le thème:
    * Mode de thème par défaut (dark/light)
    * Autorisation pour les visiteurs de changer le thème
    * Détection automatique de la langue du navigateur
  - Bouton flottant de changement de thème (avec icône soleil/lune)
  - Sauvegarde de la préférence utilisateur dans localStorage
  - CSS responsive pour le mode light avec variables CSS
  - Masquage automatique du bouton si désactivé dans les settings
- **2025-11-12: Détection automatique de langue**
  - Détection du navigator.language au premier chargement
  - Redirection automatique vers /fr ou /en selon la langue du navigateur
  - Garde avec sessionStorage pour éviter les boucles de redirection
  - Paramètre configurable dans les settings admin
- 2025-11-11: Migration complète du projet dans l'environnement Replit
- 2025-11-11: Redesign complet avec thème noir et or foncé (#B8941E) premium
- 2025-11-11: Réorganisation de la structure - templates et static à la racine
- 2025-11-11: Header transparent sauf en mode sticky avec effet de flou
- 2025-11-11: Transformation de la galerie en slider interactif de collection
- 2025-11-11: **Déplacement du carousel de collection en position haute** (après Points Forts)
- 2025-11-11: **Amélioration premium du carousel** avec badges, titres XL, boutons dégradés
- 2025-11-11: **Modernisation du footer** avec layout 4 colonnes et icônes sociales
- 2025-11-11: Ajout d'images d'arrière-plan semi-transparentes aux sections clés
- 2025-11-11: Amélioration générale du design pour un aspect plus professionnel et visuel
- 2025-11-11: Ajout de 6 nouvelles images pour la collection
- **2025-11-11: Implémentation du panneau d'administration complet**
  - Authentification sécurisée avec mot de passe environnemental
  - Gestion de contenu dynamique (CMS)
  - Upload et gestion d'images avec optimisation Pillow
  - Système de cropping d'images
  - Database models pour ContentSection, ContentField, ImageAsset, SiteSetting, AdminSession
  - Services pour content_provider, content_service, image_service
  - Templates admin avec design cohérent au thème principal
- **2025-11-11: Layout responsive "Notre Engagement"** - 3 colonnes desktop, 1 colonne mobile
- **2025-11-11: Site entièrement dynamique** - Toutes les sections (Hero, Forces, Collection, Volets, Engagement, Contact) chargent leur contenu depuis la base de données
- **2025-11-11: Ajout de tous les champs Points Forts** - Les 6 cartes de la section sont maintenant éditables via l'admin
- **2025-11-11: Optimisation SEO complète**
  - Ajout de 20+ champs SEO éditables depuis l'admin: canonical URL, robots meta, author, favicon
  - Structured Data JSON-LD avec Organization schema pour Google Search
  - Open Graph complet (OG image, type, URL, locale) pour partage social
  - Twitter Cards avec support summary_large_image
  - Fix critique: Utilisation du filtre |tojson pour le JSON-LD (évite l'échappement HTML)
  - Fix critique: Twitter meta tags utilisent name="" au lieu de property=""
- **2025-11-11: Système d'images 100% dynamique**
  - TOUTES les 18 images du site sont maintenant éditables via l'admin:
    * Hero slider (3 images)
    * Collection carousel (6 images)
    * Volets section (6 images + 1 background)
    * Engagement background
    * Footer background
  - Création du filtre Jinja personnalisé `image_url` pour gérer les images dynamiques
  - ContentProvider.get_image_url() helper method pour prioriser ImageAsset puis static paths
  - Pattern de fallback robuste: `(content.field|image_url) or url_for('static', filename='...')`
  - Ajout des champs background_image au seed pour volets, engagement et footer
- **2025-11-11: Interface Upload/Crop avancée**
  - Nouvelle page admin `/admin/upload-crop` avec Cropper.js intégration
  - Presets de dimensions pour différents formats:
    * 16:9 Hero Slider (1920x1080)
    * 4:3 Collection Cards (1200x900)
    * 1:1 Square (1080x1080)
    * Open Graph Image (1200x630)
    * Twitter Card (1200x675)
  - Crop en temps réel avec aperçu avant upload
  - Optimisation automatique des images croppées (qualité 85%, conversion RGB)
- **2025-11-12: Configuration Email/SMTP pour le formulaire de contact**
  - Nouveaux paramètres de site éditables dans `/admin/settings`:
    * Email destinataire pour les messages de contact
    * Serveur SMTP (host, port, TLS, email expéditeur)
  - Credentials SMTP sécurisés via variables d'environnement (SMTP_USERNAME, SMTP_PASSWORD)
  - Service d'envoi d'email automatique lors de la soumission du formulaire
  - Emails HTML formatés avec design professionnel
  - Validation robuste du port SMTP avec valeur par défaut (587)
  - Messages d'avertissement si la configuration SMTP est incomplète
  - Logs détaillés pour faciliter le débogage des problèmes d'envoi

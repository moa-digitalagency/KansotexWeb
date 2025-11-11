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
- Formulaire de contact fonctionnel avec stockage en base de données
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

## Accès au Panneau d'Administration
1. Accéder à `/admin/login`
2. Entrer le mot de passe (ADMIN_PASSWORD)
3. Gérer le contenu via le tableau de bord

## Démarrage
L'application démarre automatiquement via le workflow configuré qui exécute `python main.py`.

## Dernières Modifications
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
- **2025-11-11: Contenu dynamique** - Section "Notre Engagement" charge depuis la base de données

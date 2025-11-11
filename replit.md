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
  /services - Logique métier
  /utils - Utilitaires
/templates - Templates HTML (Jinja2)
/static
  /css - Styles personnalisés
  /js - JavaScript pour interactivité
  /images - Images du site (incluant images de collection et arrière-plans)
config.py - Configuration de l'application (racine)
main.py - Point d'entrée de l'application Flask
```

## Fonctionnalités
- Hero section avec slider d'images automatique (3 images)
- Header transparent qui devient opaque en mode sticky avec effet de flou
- Section "Nos Points Forts" avec les 6 atouts clés de KANSOTEX
- Section "Les volets que nous servons" avec images d'arrière-plan subtiles
- Slider de collection interactif avec navigation (6 slides, auto-play, flèches)
- Section "Notre engagement" avec images d'arrière-plan subtiles (3 piliers)
- Carousel de témoignages clients interactif
- Formulaire de contact fonctionnel avec stockage en base de données
- Footer avec image d'arrière-plan semi-transparente et 3 colonnes d'information
- Design responsive en thème noir et or foncé (#B8941E) premium
- Animations et transitions fluides
- Navigation responsive avec menu mobile

## Base de Données
### Modèle Contact
- id (Integer, clé primaire)
- name (String 100, requis)
- email (String 120, requis)
- phone (String 20, optionnel)
- message (Text, requis)
- created_at (DateTime, auto)

## Configuration
Le serveur Flask écoute sur `0.0.0.0:5000` pour permettre l'accès via le proxy Replit.

## Variables d'Environnement
- DATABASE_URL - URL de connexion PostgreSQL
- SESSION_SECRET - Clé secrète pour les sessions

## Démarrage
L'application démarre automatiquement via le workflow configuré qui exécute `python main.py`.

## Dernières Modifications
- 2025-11-11: Migration complète du projet dans l'environnement Replit
- 2025-11-11: Redesign complet avec thème noir et or foncé (#B8941E) premium
- 2025-11-11: Réorganisation de la structure - templates et static à la racine
- 2025-11-11: Header transparent sauf en mode sticky avec effet de flou
- 2025-11-11: Transformation de la galerie en slider interactif de collection
- 2025-11-11: Ajout d'images d'arrière-plan semi-transparentes aux sections clés
- 2025-11-11: Footer redesigné avec image de fond et 3 colonnes
- 2025-11-11: Amélioration générale du design pour un aspect plus professionnel et visuel
- 2025-11-11: Ajout de 6 nouvelles images pour la collection

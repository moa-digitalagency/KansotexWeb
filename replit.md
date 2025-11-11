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
  config.py - Configuration de l'application
/frontend
  /templates - Templates HTML (Jinja2)
  /static
    /css - Styles personnalisés
    /js - JavaScript pour interactivité
    /images - Images du site
main.py - Point d'entrée de l'application Flask
```

## Fonctionnalités
- Page d'accueil avec section "À propos" et expertise (+20 ans)
- Section "Les volets que nous servons" (5 catégories: Home, Hotel, Medical, Literie, Serviettes)
- Section "Nos Points Forts" avec les 5 atouts clés de KANSOTEX
- Section "Notre engagement" (3 piliers: Matériaux, Contrôle Qualité, Innovation)
- Carousel de témoignages clients interactif
- Formulaire de contact fonctionnel avec stockage en base de données
- Design responsive en thème noir et or (black & gold) premium
- Animations et transitions fluides
- README.md complet avec informations de l'entreprise

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
- 2025-11-11: Redesign complet avec thème noir et or (black & gold) premium
- 2025-11-11: Ajout de la section "Nos Points Forts" avec les 5 atouts clés
- 2025-11-11: Création du README.md avec documentation complète
- 2025-11-11: Mise à jour de tous les éléments visuels (navigation, hero, sections, footer)

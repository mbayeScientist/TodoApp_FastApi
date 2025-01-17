# FastAPI Real-Time RESTful APIs Project

Un projet backend construit avec **FastAPI**, illustrant des concepts essentiels tels que l'authentification, les relations entre tables, et la création d'API RESTful sécurisées et performantes.

## Fonctionnalités

- **Authentification et Autorisation** : Inscription, connexion, gestion des permissions avec JWT.
- **CRUD Complet** : Gestion des entités principales (Créer, Lire, Mettre à jour, Supprimer).
- **Hashage Sécurisé** : Sécurisation des mots de passe avec BCrypt.
- **Base de Données Relationnelle** : Modélisation et gestion des relations entre tables avec SQLAlchemy.
- **Validation des Données** : Gestion des schémas et validation via Pydantic.
- **Documentation Interactive** : Swagger UI disponible à `/docs`.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/mbayeScientist/TodoApp_FastApi.git
   cd nom-du-projet
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Démarrez le serveur :
   ```bash
   uvicorn main:app --reload
   ```

## Déploiement

- Le projet est prêt pour le déploiement sur **Railway** 
https://fastapitodoappbackend-production.up.railway.app/docs


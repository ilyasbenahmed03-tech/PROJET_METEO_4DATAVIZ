# Pipeline ETL Climatologie & Analytics - Departement du Rhone (1960-2026)

Ce depot contient un pipeline de Data Engineering automatise conçu pour collecter, nettoyer, enrichir et visualiser les donnees climatiques historiques de Meteo France pour le departement du Rhone.

## Presentation du Projet
L objectif de ce projet est de traiter plus de 20 005 enregistrements meteo afin d analyser les tendances climatiques a long terme (temperatures, vagues de gel et precipitations) et de fournir un tableau de bord analytique structure.

## Stack Technique
* Langage : Python 3 (Pandas, SQLAlchemy)
* Base de donnees : PostgreSQL
* Conteneurisation : Docker & Docker Compose
* Business Intelligence : Metabase

## Architecture & Voyage de la Donnee
1. Source des donnees : Donnees meteorologiques brutes de Meteo France (CSV).
2. Script ETL (etl_meteo.py) : Extrait les metriques brutes, gere les valeurs manquantes, garantit le typage strict des donnees et calcule des colonnes enrichies (amplitude thermique, frequence des mois de gel).
3. Stockage : Instance PostgreSQL dediee, herbergee dans un conteneur Docker pret pour la production.
4. Visualisation : Interface Metabase connectee directement a la base de donnees pour alimenter le tableau de bord analytique.

## Comment Lancer le Projet
Assurez-vous que Docker et Docker Compose sont bien installes sur votre systeme.

1 - Lancez l infrastructure en mode detache :
```bash
docker compose up -d
2 - Accedez a vos services :

PostgreSQL : localhost:5433

Metabase : localhost:3000

Methodologie Agile & Gestion de Projet
Ce projet a ete mene sur une periode de 5 semaines en utilisant le framework SCRUM et a ete suivi via un tableau Trello :

Sprints : Cycles de 1 semaine pour suivre les taches, de A faire (To Do) jusqu a Termine (Done).

Gestion des Risques & Pivot Agile : Lors du Sprint 5, nous avons fait face a un blocage technique majeur concernant la compatibilite des types de filtres sur Metabase (ID vs Texte). Pour respecter notre date limite de mise en production, nous avons documente l incident dans notre colonne "Bloque" et effectue un pivot Agile : nous avons contourne le filtre global du dashboard pour exploiter l interactivite native par clic sur les graphiques de Metabase afin de permettre le filtrage croise par station.

Storytelling des Donnees (Resume Executif)
Plus qu un simple pipeline technique, ce projet raconte l histoire du climat du departement du Rhone au cours des 60 dernieres annees. En transformant 20 005 donnees meteorologiques brutes en actifs structures, le pipeline met en evidence un changement climatique local clair et indeniable :

Escalade Thermique : Une augmentation constante, decennie apres decennie, des temperatures moyennes annuelles, accompagnee d une expansion majeure de l amplitude thermique annuelle.

Modeles de Pluviometrie : Un suivi precis des precipitations regionales (cumulant un total de 275,9 mm) reparties au fil des saisons pour isoler les micro-climats a travers le top 10 des stations les plus pluvieuses.

Cette architecture transforme avec succes des donnees environnementales brutes et chaotiques en une histoire automatisee et interactive, prete pour la prise de decision environnementale.

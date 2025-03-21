Système de Surveillance du Climat (Maquette)

Description

Ce projet consiste en la réalisation d'une maquette IoT dédiée à la surveillance en temps réel de la température et de l'humidité via une interface web intuitive et interactive. Le système utilise un module ESP8266 pour collecter et transmettre les données environnementales, qui sont ensuite analysées grâce à des techniques de Machine Learning pour prédire des valeurs futures et détecter des anomalies.

Fonctionnalités Principales

Acquisition en Temps Réel : collecte de données environnementales (température et humidité) à l'aide d'un module ESP8266 couplé au capteur DHT11.

Interface Web Dynamique : visualisation claire et interactive des données climatiques.

Stockage et Analyse de Données : utilisation d'algorithmes Machine Learning pour analyser, prédire les données climatiques futures et détecter des anomalies.

Visualisation Graphique : représentations graphiques interactives des données collectées et traitées.

Alertes Automatisées : notifications par e-mail, Telegram et WhatsApp en cas de valeurs climatiques anormales.

Gestion des Utilisateurs : système complet d'authentification et gestion des droits utilisateurs.

Génération de Rapports PDF : génération automatique de rapports d'historique climatique en PDF.

Technologies utilisées

Matériel : ESP8266, DHT11

Frontend : HTML, CSS, JavaScript

Backend : Django (Framework Python)

Machine Learning : Python (Scikit-learn)

Structure du projet

station_climatique/
├── capteurs/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── projet/
├── static/
├── staticfiles/
├── station_climatique/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
└── README.md

Installation et Exécution

Backend

Créez un environnement virtuel et activez-le :

python -m venv nom_env
source nom_env/bin/activate

Installez les dépendances :

pip install -r requirements.txt

Lancez les migrations :

python manage.py migrate

Lancez le serveur Django :

python manage.py runserver

Frontend

Accédez directement à l'interface web via http://localhost:8000 dans votre navigateur.

ESP8266

Chargez le fichier esp_climat.ino sur votre ESP8266 à l'aide d'Arduino IDE.

Captures d'écran

Les captures d'écran du projet sont disponibles dans le dossier assets/screens/climat.

Auteurs

Votre nom (Rôle)

Collaborateurs (si applicable)

Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.


# Système de Surveillance du Climat (Maquette)

## Description
Ce projet consiste en la réalisation d'une maquette IoT dédiée à la surveillance en temps réel de la température et de l'humidité via une interface web intuitive et interactive. Le système utilise un module ESP8266 pour collecter et transmettre les données environnementales, qui sont ensuite analysées grâce à des techniques de Machine Learning pour prédire des valeurs futures et détecter des anomalies.

## Fonctionnalités Principales
- **Acquisition en temps réel** : collecte de données environnementales (température et humidité) à l'aide d'un module ESP8266 couplé au capteur DHT11.
- **Interface web dynamique** : visualisation claire et interactive des données climatiques.
- **Stockage et analyse des données** : utilisation d'algorithmes Machine Learning pour analyser, prédire les données climatiques futures et détecter des anomalies.
- **Visualisation graphique** : représentations graphiques interactives des données collectées et traitées.
- **Alertes automatisées** : notifications par e-mail, Telegram et WhatsApp en cas de valeurs climatiques anormales.
- **Gestion des utilisateurs** : système complet d'authentification et gestion des droits utilisateurs (en cours) .
- **Génération de rapports PDF** : génération automatique de rapports d'historique climatique en PDF (en cours).

## Technologies utilisées
- **Matériel :** ESP8266, DHT11
- **Frontend :** HTML, CSS, JavaScript
- **Backend :** Django (Framework Python)
- **Machine Learning :** Python (Scikit-learn)

## Structure du projet
```
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
```

## Installation et exécution

### Backend
1. Créez un environnement virtuel et activez-le :
```bash
python -m venv nom_env
source nom_env/bin/activate
```
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```
3. Lancez les migrations :
```bash
python manage.py migrate
```
4. Lancez le serveur Django :
```bash
python manage.py runserver
```

### Frontend
- Accédez directement à l'interface web via `http://localhost:8000` dans votre navigateur.

### ESP8266
- Chargez le fichier `esp_climat.ino` sur votre ESP8266 à l'aide d'Arduino IDE.

## Captures d'écran
Les captures d'écran du projet sont disponibles dans le dossier `assets/screens/climat`.

## Auteurs
- AAZDAG ABDELLAH (Responsable)
- Collaborateurs ()

merci d ajouter vous nom !!

## Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.


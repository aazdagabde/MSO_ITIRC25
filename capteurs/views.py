import json
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from .models import DonneesCapteur
from rest_framework import generics
from .serializers import DonneesCapteurSerializer

def home(request):
    return render(request, 'capteurs/home.html')

class DonneesCapteurListCreate(generics.ListCreateAPIView):
    queryset = DonneesCapteur.objects.all()
    serializer_class = DonneesCapteurSerializer

def afficher_donnees(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_list = list(qs.values('date_heure', 'temperature', 'humidite', 'pression', 'qualite_air'))
    donnees_json = json.dumps(donnees_list, cls=DjangoJSONEncoder)
    return render(request, 'capteurs/afficher_donnees.html', {
        'donnees': qs,
        'donnees_json': donnees_json,
    })

def charts_temperature(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_list = list(qs.values('date_heure', 'temperature'))
    donnees_json = json.dumps(donnees_list, cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_temperature.html', {
        'donnees_json': donnees_json,
    })

def charts_humidite(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_list = list(qs.values('date_heure', 'humidite'))
    donnees_json = json.dumps(donnees_list, cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_humidite.html', {
        'donnees_json': donnees_json,
    })

def charts_pression(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_list = list(qs.values('date_heure', 'pression'))
    donnees_json = json.dumps(donnees_list, cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_pression.html', {
        'donnees_json': donnees_json,
    })

def charts_airquality(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_list = list(qs.values('date_heure', 'qualite_air'))
    donnees_json = json.dumps(donnees_list, cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_airquality.html', {
        'donnees_json': donnees_json,
    })

def dernieres_valeurs(request):
    try:
        derniere_donnee = DonneesCapteur.objects.latest('date_heure')
    except DonneesCapteur.DoesNotExist:
        derniere_donnee = None
    if derniere_donnee:
        time_passed = datetime.datetime.now(datetime.timezone.utc) - derniere_donnee.date_heure
    else:
        time_passed = None
    return render(request, 'capteurs/dernieres_valeurs.html', {
        'derniere_donnee': derniere_donnee,
        'time_passed': time_passed,
    })
#######################
import os
import pickle
import numpy as np
import datetime
from django.shortcuts import render
from .models import DonneesCapteur


def predict_weather(request):
    BASE_DIR = os.path.dirname(__file__)
    WEATHER_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'weather_model.pkl')
    ANOMALY_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'anomaly_model.pkl')



    # Charger le modèle de prédiction pluie
    try:
        with open(WEATHER_MODEL_PATH, 'rb') as f:
            weather_model = pickle.load(f)
    except Exception as e:
        return render(request, 'capteurs/predictions.html', {'error': "Modèle de prédiction pluie introuvable."})

    # Charger le modèle d'anomalies
    try:
        with open(ANOMALY_MODEL_PATH, 'rb') as f:
            anomaly_model = pickle.load(f)
    except Exception as e:
        return render(request, 'capteurs/predictions.html', {'error': "Modèle d'anomalies introuvable."})

    # Récupérer les 100 dernières mesures, du plus ancien au plus récent
    qs = DonneesCapteur.objects.all().order_by('-date_heure')[:100]
    if not qs:
        return render(request, 'capteurs/predictions.html', {'error': "Aucune donnée disponible."})
    qs_list = list(qs)[::-1]

    # Préparer les données pour la prédiction pluie
    X = np.array([[record.temperature, record.humidite, record.pression, record.qualite_air] for record in qs_list])
    predictions_pluie = weather_model.predict(X)

    # Détection d'anomalies sur l'ensemble des mesures
    anomalies = anomaly_model.predict(X)  # -1 indique une anomalie

    results = []
    for i, record in enumerate(qs_list):
        results.append({
            'date_heure': record.date_heure,
            'temperature': record.temperature,
            'humidite': record.humidite,
            'pression': record.pression,
            'qualite_air': record.qualite_air,
            'pluie_predite': "Pluie" if predictions_pluie[i] == 1 else "Pas de pluie",
            'anomalie': anomalies[i] == -1
        })

    context = {
        'results': results,
        'generated_at': datetime.datetime.now()
    }
    return render(request, 'capteurs/predictions.html', context)

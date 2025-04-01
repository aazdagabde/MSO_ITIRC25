import json
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .models import DonneesCapteur
from .serializers import DonneesCapteurSerializer


# Page d'accueil
def home(request):
    return render(request, 'capteurs/home.html')


# API REST pour ESP8266
# Désormais, après sauvegarde, on envoie les données à l’API externe pour obtenir la prédiction
@api_view(['POST'])
def api_reception_donnees(request):
    serializer = DonneesCapteurSerializer(data=request.data)
    if serializer.is_valid():
        donnees = serializer.save()

        payload = {
            "temperature": donnees.temperature,
            "humidite": donnees.humidite,
            "pression": donnees.pression,
            "qualite_air": donnees.qualite_air,
        }

        # Récupération de l'URL de l'API IA depuis settings.py
        from django.conf import settings
        ML_API_URL = getattr(settings, 'ML_API_URL', 'http://127.0.0.1:8001/predict')

        try:
            response = requests.post(ML_API_URL, json=payload, timeout=5)
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            return Response(
                {"error": "Erreur lors de l'appel à l'API IA", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(result, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Affichage des données
def afficher_donnees(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values()), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/afficher_donnees.html', {'donnees_json': donnees_json})


def charts_temperature(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values('date_heure', 'temperature')), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_temperature.html', {'donnees_json': donnees_json})


def charts_humidite(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values('date_heure', 'humidite')), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_humidite.html', {'donnees_json': donnees_json})


def charts_pression(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values('date_heure', 'pression')), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_pression.html', {'donnees_json': donnees_json})


def charts_airquality(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values('date_heure', 'qualite_air')), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_airquality.html', {'donnees_json': donnees_json})


def dernieres_valeurs(request):
    try:
        derniere_donnee = DonneesCapteur.objects.latest('date_heure')
    except DonneesCapteur.DoesNotExist:
        derniere_donnee = None
    time_passed = timezone.now() - derniere_donnee.date_heure if derniere_donnee else None
    return render(request, 'capteurs/dernieres_valeurs.html', {
        'derniere_donnee': derniere_donnee,
        'time_passed': time_passed,
    })


# Prédictions météo et détection d'anomalies via appel à l’API externe
def predict_weather(request):
    try:
        qs = DonneesCapteur.objects.all().order_by('-date_heure')[:100]
        if not qs:
            raise ValueError("Aucune donnée disponible")

        from django.conf import settings
        ML_API_URL = getattr(settings, 'ML_API_URL', 'http://adresse-de-votre-api/predict')

        results = []
        # Pour chaque donnée, on envoie une requête à l’API externe
        for d in reversed(qs):
            payload = {
                "temperature": d.temperature,
                "humidite": d.humidite,
                "pression": d.pression,
                "qualite_air": d.qualite_air,
            }
            try:
                response = requests.post(ML_API_URL, json=payload, timeout=5)
                response.raise_for_status()
                prediction = response.json()
            except Exception as e:
                prediction = {"error": str(e)}

            results.append({
                'date_heure': d.date_heure,
                'temperature': d.temperature,
                'humidite': d.humidite,
                'pression': d.pression,
                'qualite_air': d.qualite_air,
                'pluie_predite': "Pluie" if prediction.get("pluie") else "Pas de pluie",
                'anomalie': prediction.get("anomalie", False)
            })

        context = {'results': results, 'generated_at': timezone.now()}
        return render(request, 'capteurs/predictions.html', context)

    except Exception as e:
        return render(request, 'capteurs/predictions.html', {'error': str(e)})


class DonneesCapteurListCreate(generics.ListCreateAPIView):
    queryset = DonneesCapteur.objects.all()
    serializer_class = DonneesCapteurSerializer

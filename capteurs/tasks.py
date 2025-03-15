import os
import pickle
import numpy as np
import pandas as pd
import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import DonneesCapteur

# Chemins des fichiers modèles
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'climate_model.pkl')
ANOMALY_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'anomaly_model.pkl')

@shared_task
def retrain_model():
    """
    Récupère toutes les données, réentraîne le modèle de prédiction de température
    et sauvegarde le modèle mis à jour.
    """
    qs = DonneesCapteur.objects.all()
    if qs.exists():
        data = pd.DataFrame(list(qs.values('humidite', 'pression', 'qualite_air', 'temperature')))
        X = data[['humidite', 'pression', 'qualite_air']]
        y = data['temperature']
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        return "Modèle réentraîné avec succès"
    return "Pas de données pour réentraînement"

@shared_task
def check_anomalies_and_send_alerts():
    """
    Vérifie les 10 dernières mesures pour détecter des anomalies à l'aide du modèle
    d'anomalie et envoie une alerte par e-mail en cas d'anomalie détectée.
    """
    # Chargement (ou réentraînement) du modèle d'anomalie
    qs = DonneesCapteur.objects.all()
    if not qs.exists():
        return "Aucune donnée disponible pour la détection d'anomalie"

    data_all = pd.DataFrame(list(qs.order_by('-date_heure')[:10].values('temperature', 'humidite', 'pression', 'qualite_air')))
    # Chargement du modèle d'anomalie s'il existe
    if os.path.exists(ANOMALY_MODEL_PATH):
        with open(ANOMALY_MODEL_PATH, 'rb') as f:
            anomaly_model = pickle.load(f)
    else:
        # Sinon, entraînement initial
        from sklearn.ensemble import IsolationForest
        anomaly_model = IsolationForest(contamination=0.05, random_state=42)
        full_data = pd.DataFrame(list(qs.values('temperature', 'humidite', 'pression', 'qualite_air')))
        anomaly_model.fit(full_data)
        with open(ANOMALY_MODEL_PATH, 'wb') as f:
            pickle.dump(anomaly_model, f)

    predictions = anomaly_model.predict(data_all)
    anomalies = data_all[predictions == -1]
    if not anomalies.empty:
        subject = "Alerte Anomalie - Station Climatique"
        message = f"Des anomalies ont été détectées dans les mesures récentes:\n\n{anomalies.to_string(index=False)}"
        recipient_list = [settings.ALERT_EMAIL]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    return "Tâche d'alerte exécutée"

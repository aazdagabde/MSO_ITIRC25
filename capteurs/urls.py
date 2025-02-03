from django.urls import path
from . import views
from .views import DonneesCapteurListCreate


urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('donnees/', views.afficher_donnees, name='afficher_donnees'),
    path('api/donnees/', DonneesCapteurListCreate.as_view(), name='donnees-capteur-list'),
]
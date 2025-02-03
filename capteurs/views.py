
from django.shortcuts import render
from .models import DonneesCapteur


from django.shortcuts import render
from .models import DonneesCapteur

def home(request):
    return render(request, 'capteurs/home.html')

from rest_framework import generics
from .models import DonneesCapteur
from .serializers import DonneesCapteurSerializer

class DonneesCapteurListCreate(generics.ListCreateAPIView):
    queryset = DonneesCapteur.objects.all()
    serializer_class = DonneesCapteurSerializer

def afficher_donnees(request):
    donnees = DonneesCapteur.objects.all().order_by('-date_heure')
    return render(request, 'capteurs/afficher_donnees.html', {'donnees': donnees})
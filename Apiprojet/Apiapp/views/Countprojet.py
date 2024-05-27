from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Projet
from django.db.models import Sum

class CountProjet(APIView):
    def get(self, request):
       
        nombre_projets = Projet.objects.count()
        
    
        return Response({'nombre_projets': nombre_projets})
class CountMontant(APIView):
    def get(self, request):
        montant_total = Projet.objects.aggregate(total_montant=Sum('montant_ht'))['total_montant']
        return Response({'montant_total': montant_total})
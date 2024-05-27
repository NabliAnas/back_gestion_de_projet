from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from ..models import Projet
from ..serializers.projetser import ProjetSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class UpdateProjetTaux(APIView):
    def put(self, request, pk):
        try:
            projet = Projet.objects.get(pk=pk)
        except Projet.DoesNotExist:
            raise Http404
        data = request.data
        ancien_taux_realisation = data.get('ancien_taux_realisation')
        new_taux_realisation = data.get('new_taux_realisation')
        print(new_taux_realisation)
        if ancien_taux_realisation is not None:
            projet.ancien_taux_realisation = ancien_taux_realisation

        if new_taux_realisation is not None:
            projet.new_taux_realisation = new_taux_realisation
            print(new_taux_realisation)
            if new_taux_realisation == "100":
                projet.statut = 1
            else:
                projet.statut = 0
        projet.save()
        return Response(status=status.HTTP_200_OK)

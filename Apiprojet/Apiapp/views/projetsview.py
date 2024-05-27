from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from ..models import Projet,Facture
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers.projetser import ProjetSerializer
from ..serializers.userser import UserSerializer
from django.contrib.auth import get_user_model
from num2words import num2words
class Projetcreate(APIView):
    def get(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        User = get_user_model() 
        Bu_managers = User.objects.filter(id_role=2)
        années = Projet.objects.order_by('Annee').values_list('Annee', flat=True).distinct()
        if user.id_role_id != 2:
            projects = Projet.objects.all()
        else:
            projects = Projet.objects.filter(id_user=user.id)
        projet_serializer = ProjetSerializer(projects, many=True)  
        user_serializer = UserSerializer(Bu_managers, many=True)  
        return Response({'projects': projet_serializer.data, 'years': années, 'Bu_managers': user_serializer.data})
    def post(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        data = request.data
        serializer = ProjetSerializer(data=data)
        if serializer.is_valid():
            User = get_user_model()  
            user_instance = User.objects.get(pk=user.id)  
            projet = serializer.save(id_user=user_instance)  
            return Response({'success': True, 'message': 'Projet créé avec succès', 'id': projet.id_projet}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        try:
            projet = Projet.objects.get(pk=pk)
            serializer = ProjetSerializer(projet, data=request.data, partial=True)
            if serializer.is_valid():
                updated_projet = serializer.save()
                facture = Facture.objects.get(id_projet=pk)
                facture.total_ht = updated_projet.montant_ht
                facture.total_tva = updated_projet.montant_ht * 0.2
                facture.total_ttc = updated_projet.montant_ht * 1.2
                facture.unite = updated_projet.mode_facturation
                facture.numword = num2words(facture.total_ttc, lang='fr')
                if updated_projet.mode_facturation == 'JH':
                    facture.prix_unitaire = updated_projet.tarif
                    facture.quantite = updated_projet.nbrJh
                facture.save()
                return Response({'success': True, 'message': 'Projet mis à jour avec succès'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Projet.DoesNotExist:
            raise Http404
    def delete(self, request, pk):
        try:
            projet = Projet.objects.get(pk=pk)
            projet.delete()
            return Response({'success': True, 'message': 'Projet supprimé avec succès'})
        except Projet.DoesNotExist:
            raise Http404
class Projetf(APIView):
    def get(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        User = get_user_model() 
        Bu_managers = User.objects.filter(id_role=2)
        années = Projet.objects.order_by('facturation').values_list('Annee', flat=True).distinct()
        if user.id_role_id != 2:
            projects = Projet.objects.all().order_by('-facturation', '-recouvrement')
        else:
            projects = Projet.objects.filter(id_user=user.id).order_by('-facturation', '-recouvrement')
        projet_serializer = ProjetSerializer(projects, many=True)  
        user_serializer = UserSerializer(Bu_managers, many=True)  
        return Response({'projects': projet_serializer.data, 'years': années, 'Bu_managers': user_serializer.data})
class Recouvrement(APIView):
    def put(self, request, pk):
            projet = Projet.objects.get(pk=pk)
            projet.recouvrement=1
            projet.save()
            return Response({'success': True, 'message': 'revouvreee'})
class FilterByYear(APIView):
    def post(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        User = get_user_model()
        Bu_managers = User.objects.filter(id_role=2)
        années = Projet.objects.order_by('Annee').values_list('Annee', flat=True).distinct()
        if user.id_role_id != 2:
            projects = Projet.objects.filter(Annee=request.data.get('filteryear')).order_by('date_creation')
        else:
            projects = Projet.objects.filter(id_user=user.id,Annee=request.data.get('filteryear')).order_by('date_creation')
        projet_serializer = ProjetSerializer(projects, many=True)
        user_serializer = UserSerializer(Bu_managers, many=True)
        return Response({'projects': projet_serializer.data, 'years': années, 'Bu_managers': user_serializer.data})

class FilterByManager(APIView):
    def post(self, request):
        User = get_user_model()
        Bu_managers = User.objects.filter(id_role=2)
        années = Projet.objects.order_by('Annee').values_list('Annee', flat=True).distinct()
        projects = Projet.objects.filter(id_user=request.data.get('filterbu')).order_by('date_creation')
        projet_serializer = ProjetSerializer(projects, many=True)
        user_serializer = UserSerializer(Bu_managers, many=True)
        return Response({'projects': projet_serializer.data, 'years': années, 'Bu_managers': user_serializer.data})

class FilterByStatus(APIView):
    def post(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        User = get_user_model()
        Bu_managers = User.objects.filter(id_role=2)
        années = Projet.objects.order_by('Annee').values_list('Annee', flat=True).distinct()
        if user.id_role_id != 2:
            projects = Projet.objects.filter(statut=request.data.get('filterstatut')).order_by('date_creation')
        else:
            projects = Projet.objects.filter(id_user=user.id,statut=request.data.get('filterstatut')).order_by('date_creation')
        projet_serializer = ProjetSerializer(projects, many=True)
        user_serializer = UserSerializer(Bu_managers, many=True)
        return Response({'projects': projet_serializer.data, 'years': années, 'Bu_managers': user_serializer.data})
class Getrole(APIView):
    def get(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        User = get_user_model()
        return Response({'idrole': user.id_role_id})
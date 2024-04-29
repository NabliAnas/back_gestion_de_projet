from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from ..models import Projet
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers.projetser import ProjetSerializer
from ..serializers.userser import UserSerializer
from django.contrib.auth import get_user_model
class Projetcreate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        User = get_user_model() 
        Bu_managers = User.objects.filter(id_role=2)
        années = Projet.objects.order_by('Annee').values_list('Annee', flat=True).distinct()
        if user.id_role != 2:
            projects = Projet.objects.all()
        else:
            projects = Projet.objects.filter(id_user=user.id)
        projet_serializer = ProjetSerializer(projects, many=True)  
        user_serializer = UserSerializer(Bu_managers, many=True)  
        return Response({'projects': projet_serializer.data, 'Années': années, 'Bu_managers': user_serializer.data})

    def post(self, request):
        
        user = JWTAuthentication().authenticate(request)[0]
        data = request.data
        serializer = ProjetSerializer(data=data)
        if serializer.is_valid():
            User = get_user_model()  
            user_instance = User.objects.get(pk=user.id)  
            serializer.save(id_user=user_instance)  
            return Response({'success': True, 'message': 'Projet créé avec succès'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        try:
            projet = Projet.objects.get(pk=pk)
            serializer = ProjetSerializer(projet, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
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

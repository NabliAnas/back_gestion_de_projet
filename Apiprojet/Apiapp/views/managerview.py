from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from ..models import User
from ..serializers.managerser import UserSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import status
class UserList(APIView):
    def get(self, request):
        users = User.objects.all().order_by('id_role')
        data = [{'id': user.id, 'username': user.username, 'email': user.email,'city':user.city, 'id_role': user.id_role} for user in users]
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)
    def put(self, request, id):
        user = get_object_or_404(User, pk=id) 
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Role updated successfully for user with ID {user.id}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class UserCount(APIView):
    def get(self, request):
        user_count = User.objects.count()
        return Response({'user_count': user_count})
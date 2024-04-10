from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import User
from ..serializers.managerser import UserSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import status


class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        data = [{'id': user.id, 'username': user.username, 'email': user.email, 'id_role': user.id_role} for user in users]
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

class UserManagerUpdateAPIView(APIView):
    def post(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Role updated successfully for user with ID {user.id}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserManagerDestroyAPIView(APIView):
    def post(self, request, id):
        role = get_object_or_404(User, pk=id)
        role.delete()
        return Response({'message': 'Role deleted successfully'})




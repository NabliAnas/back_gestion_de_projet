from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from ..serializers.userser import UserSerializer
from ..models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Incorrect email or password!')
        token = AccessToken.for_user(user)
        response = Response({'token': str(token)})
        response.set_cookie(key='jwt', value=str(token), httponly=True)
        return response
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
class UserViewp(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        serializer = UserSerializer(user)
        return Response(serializer.data)
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        return response

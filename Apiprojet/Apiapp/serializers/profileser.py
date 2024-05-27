from rest_framework import serializers
from ..models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', 'email', 'address', 'city', 'country', 'postal', 'about']

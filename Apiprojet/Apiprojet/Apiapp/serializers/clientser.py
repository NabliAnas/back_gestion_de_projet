from rest_framework import serializers
from ..models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'raison_sociale', 'responsable', 'email', 'adresse', 'telephone', 'created_at', 'updated_at']

from rest_framework import serializers
from ..models import Projet

class ProjetSerializer(serializers.ModelSerializer):
    def calculate_montant_ht(self, validated_data):
            nbrJh = validated_data.get('nbrJh')
            tarif = validated_data.get('tarif')
            return nbrJh * tarif
    def create(self, validated_data):
        mode_facturation = validated_data.get('mode_facturation')
        if mode_facturation == 'JH':
            validated_data['montant_ht'] = self.calculate_montant_ht(validated_data)
        return super().create(validated_data)
    def update(self, instance, validated_data):
        mode_facturation = validated_data.get('mode_facturation')
        if mode_facturation == 'JH':
            validated_data['montant_ht'] = self.calculate_montant_ht(validated_data)
        return super().update(instance, validated_data)
    class Meta:
        model = Projet
        fields = '__all__'

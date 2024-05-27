from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Projet, Facture
from ..serializers.factureser import FactureSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import time
from num2words import num2words

class FactureCreate(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            factures = Facture.objects.all()
            if not factures.exists():
                return Response({'error': 'No Facture found for this Projet'}, status=status.HTTP_404_NOT_FOUND)
            serializer = FactureSerializer(factures, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Projet.DoesNotExist:
            return Response({'error': 'Projet not found'}, status=status.HTTP_404_NOT_FOUND)

    def generate_reference(self):
        return 'REF' + str(int(time.time()))

    def post(self, request, id):
        try:
            projet = Projet.objects.get(pk=id)
            total_ht = projet.montant_ht
            total_tva = total_ht * 0.2
            total_ttc = total_ht * 1.2

            facture_data = {
                'id_projet': projet.id_projet,
                'prix_unitaire': total_ht,
                'total_tva': total_tva,
                'total_ht': total_ht,
                'total_ttc': total_ttc,
                'unite': projet.mode_facturation,
                'numword': num2words(total_ttc, lang='fr'),
                'reference': self.generate_reference()
            }

            if projet.mode_facturation == 'JH':
                facture_data['prix_unitaire'] = projet.tarif
                facture_data['quantite'] = projet.nbrJh

            serializer = FactureSerializer(data=facture_data)
            if serializer.is_valid():
                serializer.save()
                projet.facturation = True
                projet.save()
                return Response({'success': True, 'message': 'Facture créée avec succès'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Projet.DoesNotExist:
            return Response({'error': 'Projet not found'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Client
from ..serializers.clientser import ClientSerializer
class ClientViewSet(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = Client.objects.get(pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class ClientViewSet2(APIView):
    def get(self, request, pk):
            try:
                client = Client.objects.get(pk=pk)
                return Response({'raison_sociale': client.raison_sociale})
            except Client.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
class ClientCountView(APIView):  
    def get(self, request):
        client_count = Client.objects.count()
        return Response({'client_count': client_count})
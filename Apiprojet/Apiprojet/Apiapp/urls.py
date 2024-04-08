from django.urls import path,include 
from .views.authview import RegisterView, LoginView, UserView, LogoutView
from rest_framework.routers import DefaultRouter
from .views.clientview import ClientViewSet


urlpatterns = [
    path('clients/', ClientViewSet.as_view(), name='client-list'),  # For GET and POST requests
    path('clients/<int:pk>/', ClientViewSet.as_view(), name='client-detail'),  # For PUT and DELETE requests
]

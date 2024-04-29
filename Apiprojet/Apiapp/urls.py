from django.urls import path,include 
from .views.authview import RegisterView, LoginView, UserView, LogoutView
from rest_framework.routers import DefaultRouter
from .views.clientview import ClientViewSet,ClientViewSet2
from .views.managerview import UserList
from .views.projetsview import Projetcreate
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    #clients 
    path('clients/', ClientViewSet.as_view(), name='client-list'),  # For GET and POST requests
    path('clients/<int:pk>/', ClientViewSet.as_view(), name='client-detail'),
    path('clients/show/<int:pk>/', ClientViewSet2.as_view(), name='client-show'),
    # users
    path('users/', UserList.as_view(), name='roles-list'),
    path('users/<int:id>/', UserList.as_view(), name='role-update'),
    path('users/delete/<int:pk>/', UserList.as_view(), name='user-delete'),
    # projets
    path('projets/', Projetcreate.as_view(), name='projetcreate'),
    path('projets/<int:pk>/', Projetcreate.as_view(), name='projetupdate'),
    path('projets/<int:pk>/delete/', Projetcreate.as_view(), name='projetdelete'),
]


from django.urls import path,include 
from .views.authview import RegisterView, LoginView, UserView, LogoutView,UserViewp
from rest_framework.routers import DefaultRouter
from .views.clientview import ClientViewSet,ClientViewSet2
from .views.managerview import UserList
from .views.factureview import FactureCreate
from .views.etatavancement import UpdateProjetTaux
from .views.profileview import UserProfileUpdate
from .views.projetsview import Projetcreate,FilterByManager,FilterByStatus,FilterByYear,Getrole,Projetf,Recouvrement
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('user/profile/', UserViewp.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', UserProfileUpdate.as_view(), name='profile-update'),
    #clients 
    path('clients/', ClientViewSet.as_view(), name='client-list'),  # For GET and POST requests
    path('clients/<int:pk>/', ClientViewSet.as_view(), name='client-detail'),
    path('clients/show/<int:pk>/', ClientViewSet2.as_view(), name='client-show'),
    # users
    path('users/', UserList.as_view(), name='roles-list'),
    path('users/<int:id>/', UserList.as_view(), name='role-update'),
    path('users/delete/<int:pk>/', UserList.as_view(), name='user-delete'),
    # projets
    path('projets/', Projetcreate.as_view(), name='projet'),
    path('projetsf/', Projetf.as_view(), name='projetf'),
    path('projets/<int:pk>/', Projetcreate.as_view(), name='projetupdate'),
    path('recouvrement/<int:pk>/', Recouvrement.as_view(), name='projetupdate'),
    path('projets/<int:pk>/delete/', Projetcreate.as_view(), name='projetdelete'),
    #facture
    path('createfacture/<int:id>/', FactureCreate.as_view(), name='create-facture'),
    path('factures/', FactureCreate.as_view(), name='create-facture'),
    #filtres
    path('filterbu/', FilterByManager.as_view(), name='FilterByManager'),
    path('filterstatut/', FilterByStatus.as_view(), name='FilterByStatus'),
    path('filteryear/', FilterByYear.as_view(), name='FilterByYear'),
    #GETROLE
    path('getrole/', Getrole.as_view(), name='getrole'),
    #etatavancement
    path('etatavancement/<int:pk>/', UpdateProjetTaux.as_view(), name='update_projet_taux')
]


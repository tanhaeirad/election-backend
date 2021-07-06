from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView, UserListView

urlpatterns = [
    path('login/', view=obtain_auth_token, name='account-login'),
    path('register/', view=RegisterView.as_view(), name='account-register'),
    path('users/', view=UserListView.as_view(), name='account-user-list'),
]

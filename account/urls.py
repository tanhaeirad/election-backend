from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView, UserListView, RetrieveCurrentUserView, RetrieveUserView

urlpatterns = [
    path('login/', view=obtain_auth_token, name='account-login'),
    path('register/', view=RegisterView.as_view(), name='account-register'),
    path('users/<int:user_id>/', view=RetrieveUserView.as_view(), name='account-user-retrieve'),
    path('users/', view=UserListView.as_view(), name='account-user-list'),
    path('users/me/', view=RetrieveCurrentUserView.as_view(), name='account-user-current'),
]

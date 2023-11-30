# accounts/urls.py
from django.urls import path
from .views import CustomUserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, signup_view

urlpatterns = [
    path('users/', CustomUserViewSet.as_view(), name='user-list'),
    path('signup/', signup_view, name='signup'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
]

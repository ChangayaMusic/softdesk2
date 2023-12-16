# accounts/urls.py
from django.urls import path
from .views import CustomUserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, signup_view
from .views import ModifyUserView, DeleteUserView

urlpatterns = [
    path('users/', CustomUserViewSet.as_view(), name='user-list'),
    path('signup/', signup_view, name='signup'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('modify-user/<int:id>/', ModifyUserView.as_view(), name='modify-user'),
    path('delete-user/<int:id>/', DeleteUserView.as_view(), name='delete-user'),
]

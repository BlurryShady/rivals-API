from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ProfileAvatarUpdateView,
    PublicProfileView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile/avatar/', ProfileAvatarUpdateView.as_view()),
    path('users/<str:username>/', PublicProfileView.as_view()),
]
from django.urls import path

from apps.website.views import Home, Auth

urlpatterns = [
    path('', Home.as_view()),
    path('auth', Auth.as_view()),
]
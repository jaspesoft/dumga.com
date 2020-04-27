from django.urls import path

from apps.website.views import Home

urlpatterns = [
    path('', Home.as_view()),
]
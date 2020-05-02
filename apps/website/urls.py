from django.urls import path

from apps.website.views import *

urlpatterns = [
    path('', Home.as_view()),
    path('auth/signup', AuthSignUp.as_view()),
    path('auth/signin', AuthSignin.as_view()),
]
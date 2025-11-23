from django.urls import path
from .views import MainPageView


app_name = "core"

urlpatterns = [
    path('',MainPageView.as_view(),name='home-page')
]
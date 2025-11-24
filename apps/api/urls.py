from django.urls import path
from .views import FakeUsersView,FakeArticleView


app_name = "api"
urlpatterns = [
    path("fake_users/<int:count>/",FakeUsersView.as_view()),
    path("fake_articles/<int:count>/",FakeArticleView.as_view()),
]
from django.urls import path
from .views import FrontFakeObjectsView


app_name = "api"
urlpatterns = [
    path("front_json_placeholder/<int:count_article>/<int:count_user>",FrontFakeObjectsView.as_view()),
]
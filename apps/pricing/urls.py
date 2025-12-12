from django.urls import path
from . import views


app_name = "subscription"

urlpatterns = [
    path("", views.SubscriptionPlanListView.as_view(), name="sub-plans"),
]

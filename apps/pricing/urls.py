from django.urls import path
from . import views


app_name = "pricing"

urlpatterns = [
    path("subscription/plans/", views.SubscriptionPlanListView.as_view(), name="sub-plans"),
]

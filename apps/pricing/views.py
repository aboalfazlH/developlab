from django.views.generic import ListView
from .models import Subscription,SubscriptionPlan


class SubscriptionPlanListView(ListView):
    model = SubscriptionPlan
    template_name = "sub-plans.html"
    context_object_name = "sub_plans"
    def get_queryset(self):
        return SubscriptionPlan.objects.all().order_by("value")
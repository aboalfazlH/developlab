from django.db import models
from apps.accounts.models import CustomUser

class SubscriptionPlan(models.Model):
    """Model definition for SubscriptionPlan."""

    plan_name = models.CharField()

    class Meta:
        """Meta definition for SubscriptionPlan."""

        verbose_name = 'پلن اشتراک'
        verbose_name_plural = 'پلن های اشتراک'

    def __str__(self):
        """Unicode representation of SubscriptionPlan."""
        return self.plan_name    

class Subscription(models.Model):
    """Model definition for Subscription."""
    subscription_plan = models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE)
    subscription_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    class Meta:
        """Meta definition for Subscription."""

        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        """Unicode representation of Subscription."""
        f"{self.subscription_user}-{self.subscription_plan}|{self.start_date} تا {self.end_date}"

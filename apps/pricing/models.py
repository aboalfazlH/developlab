from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class SubscriptionPlan(models.Model):
    plan_name = models.CharField(verbose_name="نام پلن")
    real_name = models.CharField(verbose_name="نام پلن")
    price = models.PositiveIntegerField(verbose_name="قیمت", default=0)
    value = models.PositiveIntegerField(verbose_name="ارزش پلن", default=0)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    articles = models.CharField(verbose_name="وضعیت مقالات", blank=True, null=True)
    questions = models.CharField(verbose_name="وضعیت پرسش ها", blank=True, null=True)
    private_projects = models.CharField(verbose_name="وضعیت پروژه های خصوصی", blank=True, null=True)

    class Meta:
        verbose_name = "پلن اشتراک"
        verbose_name_plural = "پلن های اشتراک"

    def __str__(self):
        return self.plan_name


class Subscription(models.Model):
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE, verbose_name="پلن اشتراک"
    )
    subscription_user = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر"
    )
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")

    @property
    def is_active(self):
        return self.end_date >= timezone.now()

    class Meta:
        verbose_name = "اشتراک"
        verbose_name_plural = "اشتراک ها"

    def save(self, *args, **kwargs):
        if (
            Subscription.objects.filter(
                subscription_user=self.subscription_user, end_date__gte=timezone.now()
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValueError(
                "این کاربر یک اشتراک فعال دارد و نمی‌تواند اشتراک جدید بگیرد."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        start = self.start_date.strftime("%Y-%m-%d %H:%M")
        end = self.end_date.strftime("%Y-%m-%d %H:%M")
        return f"{self.subscription_user.get_full_name()} | {self.subscription_plan} | {start} تا {end}"


class Product(models.Model):
    PRODUCT_TYPES = [
        ('subscription', 'اشتراک'),
    ]
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.product_type})"


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.active and self.expires_at >= timezone.now()

    def __str__(self):
        return self.code


class DiscountItem(models.Model):
    discount_code = models.ForeignKey(
        DiscountCode, on_delete=models.CASCADE, related_name='items'
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    discount_percent = models.PositiveIntegerField()

    def applies_to(self, item):
        """چک می‌کند که این تخفیف روی این آیتم اعمال می‌شود یا نه"""
        if self.content_object.id == item.id:
            return True
        if self.content_object is None and self.min_price and getattr(item, 'price', 0) >= self.min_price:
            return True
        return False

    def __str__(self):
        target = str(self.content_object) if self.content_object else f"Price >= {self.min_price}"
        return f"{self.discount_percent}% تخفیف روی {target}"


class DiscountCodeUsage(models.Model):
    discount_code = models.ForeignKey(
        DiscountCode, on_delete=models.CASCADE, related_name='usages'
    )
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('discount_code', 'user')

    def __str__(self):
        return f"{self.user.username} used {self.discount_code.code}"

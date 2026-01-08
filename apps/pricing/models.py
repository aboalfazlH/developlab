from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import FileExtensionValidator
from django.db.models import Count, Max


def course_thumbnail_upload_path(instance,filename):
    now = timezone.now()
    return f"pricing/courses/thumbnails/{now.year:04}{now.month:02}{now.day:02}{now.second:02}/{filename}"

class SubscriptionPlan(models.Model):
    plan_name = models.CharField(verbose_name="نام پلن")
    real_name = models.CharField(verbose_name="نام واقعی پلن")
    price = models.PositiveIntegerField(verbose_name="قیمت", default=0)
    value = models.PositiveIntegerField(verbose_name="ارزش پلن", default=0)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    description = models.TextField(blank=True,null=True)

    @property
    def is_most_popular(self):
        subscriptions_with_counts = Subscription.objects.values('subscription_plan') \
            .annotate(_count=Count('subscription_user'))
        
        max_count = subscriptions_with_counts.aggregate(max_s=Max('_count'))['max_s'] or 0
        
        current_count = next(
            (item['_count'] for item in subscriptions_with_counts if item['subscription_plan'] == self.id), 
            0
        )
        
        return current_count == max_count

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

    @property
    def time_remaining(self):
        now = timezone.now()

        if now >= self.end_date:
            return "منقضی 🟠"

        remaining = self.end_date - now

        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        return f"{days} روز، {hours} ساعت، {minutes} دقیقه"

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


class Course(models.Model):
    PAID_TYPES = [
        ('paid', 'تمام پولی'),
        ('semi_paid', 'نیمه پولی'),
        ('free', 'رایگان'),
    ]
    COURSE_TYPES = [
        ('basic', 'مقدماتی'),
        ('advanced', 'پیشرفته'),
        ('basic2advanced', 'مقدماتی تا پیشرفته'),
        ('one2hundred', 'صفر تا صد'),
    ]
    title = models.CharField(verbose_name="موضوع",max_length=300)
    slug = models.SlugField(verbose_name="شناسه",unique=True)
    summary = models.TextField(verbose_name="خلاصه",blank=True,null=True)
    description = models.TextField(verbose_name="توضیحات",blank=True,null=True)
    thumbnail = models.ImageField(verbose_name="تصویر بند انگشتی",upload_to=course_thumbnail_upload_path,blank=True,null=True)
    preview = models.FileField(
    verbose_name="پیش نمایش",
    blank=True,
    null=True,
    validators=[FileExtensionValidator(
        allowed_extensions=['MOV','avi','mp4','webm','mkv']
    )],
    )
    paid_type = models.CharField(verbose_name="نوع قیمت دوره",choices=PAID_TYPES)
    course_type = models.CharField(verbose_name="نوع دوره",choices=COURSE_TYPES)
    price = models.PositiveIntegerField(verbose_name="قیمت",default=0)
    teacher = models.ForeignKey("accounts.CustomUser",on_delete=models.CASCADE,verbose_name="مدرس")
    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="دوره")
    title = models.CharField(verbose_name="موضوع",max_length=300)
    slug = models.SlugField(verbose_name="شناسه",unique=True)
    summary = models.TextField(verbose_name="خلاصه",blank=True,null=True)
    thumbnail = models.ImageField(verbose_name="تصویر بند انگشتی",upload_to=course_thumbnail_upload_path,blank=True,null=True)
    video = models.FileField(
    verbose_name="ویدیو",
    blank=True,
    null=True,
    validators=[FileExtensionValidator(
        allowed_extensions=['MOV','avi','mp4','webm','mkv']
    )],
    )
    price = models.PositiveIntegerField(verbose_name="قیمت")
    attached_file = models.FileField(verbose_name="فایل ضمیمه")

    def __str__(self):
        return self.title


class Product(models.Model):
    PRODUCT_TYPES = [
        ('subscription', 'اشتراک'),
        ('course', 'دوره ها'),
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
        return f"{self.user.name} used {self.discount_code.code}"


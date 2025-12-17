from social_django.models import UserSocialAuth, Association, Nonce


class UserSocialAuthProxy(UserSocialAuth):
    class Meta:
        proxy = True
        verbose_name = "حساب اجتماعی کاربر"
        verbose_name_plural = "حساب‌های اجتماعی کاربران"


class AssociationProxy(Association):
    class Meta:
        proxy = True
        verbose_name = "ارتباط OAuth"
        verbose_name_plural = "ارتباط‌های OAuth"


class NonceProxy(Nonce):
    class Meta:
        proxy = True
        verbose_name = "توکن موقت"
        verbose_name_plural = "توکن‌های موقت"
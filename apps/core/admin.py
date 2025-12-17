from django.contrib import admin
from .models import LinkModel, Category
from .admin_site import admin_site
from .proxies.social_auth import (
    UserSocialAuthProxy,
    AssociationProxy,
    NonceProxy,
)

@admin.register(LinkModel,site=admin_site)
class LinkModelAdmin(admin.ModelAdmin):
    """Admin View for LinkModel"""

    list_display = ("name",)
    search_fields = ("name",)
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

@admin.register(Category,site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    """Admin View for Category"""

    list_display = ("name",)
    search_fields = ("name",)
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass



@admin.register(UserSocialAuthProxy, site=admin_site)
class UserSocialAuthAdmin(admin.ModelAdmin):
    list_display = ("user", "provider", "uid")
    search_fields = ("user__username", "uid")
    ordering = ("user",)


@admin.register(AssociationProxy, site=admin_site)
class AssociationAdmin(admin.ModelAdmin):
    pass


@admin.register(NonceProxy, site=admin_site)
class NonceAdmin(admin.ModelAdmin):
    pass


from social_django.models import UserSocialAuth, Association, Nonce


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

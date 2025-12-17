from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import AlreadyRegistered


EXCLUDED_APP_LABELS = {
    "social_django",
}


class DevlabAdminSite(AdminSite):
    site_header = "ادمین آزمایشگاه توسعه"
    site_title = "آزمایشگاه توسعه"
    index_title = "مدیریت"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        priority = [
            "core",
            "accounts",
            "content",
            "communications",
        ]

        def app_order(app):
            try:
                return priority.index(app["app_label"])
            except ValueError:
                return 999

        app_list.sort(key=lambda app: (app_order(app), app["name"]))
        return app_list


def clone_default_admin_site(custom_site):
    """
    Clone all models registered on Django's default admin site
    into the given custom AdminSite, excluding selected apps.
    """
    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label

        if app_label in EXCLUDED_APP_LABELS:
            continue

        admin_class = model_admin.__class__

        try:
            custom_site.register(model, admin_class)
            new_admin = custom_site._registry[model]

            for attr, value in vars(model_admin).items():
                if not attr.startswith("_"):
                    setattr(new_admin, attr, value)

        except AlreadyRegistered:
            continue


admin_site = DevlabAdminSite(name="admin")
clone_default_admin_site(admin_site)

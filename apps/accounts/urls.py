from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("users/", views.CustomUserListView.as_view(), name="users"),
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("edit/", views.CustomUserUpdateView.as_view(), name="users-profile-edit"),

    path("password-change/", auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html"
    ), name="password_change"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"
    ), name="password_change_done"),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path("<str:username>/follow/", views.FollowView.as_view(), name="user-follow"),
    path("<str:username>/followers/", views.CustomUserFollowersListView.as_view(), name="followers"),
    path("<str:username>/following/", views.CustomUserFollowingListView.as_view(), name="following"),
    path("<str:username>/", views.ProfileDetailView.as_view(), name="users-profile"),

    path("", views.ProfileDetailView.as_view(), name="user-profile"),
]

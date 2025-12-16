from django.views.generic import CreateView, FormView, DetailView, UpdateView, ListView,View
from .forms import CustomUserCreationForm, LoginForm, ProfileEditForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, ProfileLink
from django.shortcuts import get_object_or_404
from apps.blog.models import Article
from django.urls import reverse_lazy
from django.contrib import messages


class SignUpView(CreateView):
    """form for signup user"""

    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("core:home-page")
    template_name = "accounts/auth/sign-up.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "شما اکنون احراز هویت کردید")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """login user if form is valid"""
        response = super().form_valid(form)

        login(
            self.request,
            self.object,
            backend="django.contrib.auth.backends.ModelBackend",
        )

        return response


class LoginView(FormView):
    """Login user using email and password"""

    form_class = LoginForm
    template_name = "accounts/auth/login.html"
    success_url = reverse_lazy("core:home-page")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        account = CustomUser.objects.filter(email=email).first()

        if not account:
            form.add_error(None, "ایمیل یا رمز عبور اشتباه است.")
            return self.form_invalid(form)

        if not account.has_usable_password():
            form.add_error(None, "شما باید با گیت هاب وارد شود")
            return self.form_invalid(form)

        user = authenticate(email=account.email, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"خوش آمدید {user}")
            return super().form_valid(form)
        form.add_error(None, "ایمیل یا رمز عبور اشتباه است.")
        return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        """Redirect authenticated users to home page"""
        if request.user.is_authenticated:
            messages.warning(request, "شما اکنون احراز هویت کردید")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class CustomLogoutView(LoginRequiredMixin, FormView):
    success_url = reverse_lazy("core:home-page")

    def get(self, request, *args, **kwargs):
        return render(request, "accounts/auth/logout-confirm.html")

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "با موفقیت خارج شدید")
        return redirect(self.success_url)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """User profile"""
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        username = self.kwargs.get(self.slug_url_kwarg)

        if username:
            # Perform a case-insensitive exact match on username (e.g., "Ali" matches "ali", "ALI", etc.)
            return get_object_or_404(CustomUser, username__iexact=username)

        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["profile"]

        context["articles"] = Article.objects.filter(
            author=user, is_active=True
        ).order_by("-write_date", "-views")[:10]

        context["links"] = ProfileLink.objects.filter(user=user)

        return context


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = "accounts/user_update_profile.html"
    form_class = ProfileEditForm
    success_url = reverse_lazy("user-profile")

    def get_object(self, queryset=None):
        """User only can edit yourself profile"""
        return self.request.user

class FollowView(View):
    def post(self, request, username, *args, **kwargs):
        target_user = CustomUser.objects.get(username=username)
        current_user = request.user

        if current_user.is_following(target_user):
            messages.success(request,"دیگر شما این کاربر را دنبال نمیکنید")
            current_user.following.remove(target_user)

        else:
            messages.success(request,"دنبال کردن کاربر موفق بود")
            current_user.following.add(target_user)

        return redirect(request.META.get("HTTP_REFERER", "/"))


class CustomUserListView(ListView):
    model = CustomUser
    template_name = "accounts/users.html"
    context_object_name = "users"
    paginate_by = 100

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True).order_by("-last_login")


class CustomUserFollowersListView(ListView):
    """
    Display a list of users who follow the given user.
    """
    model = CustomUser
    template_name = "accounts/users.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        """
        Return followers of the target user.
        """
        self.profile_user = get_object_or_404(
            CustomUser, username=self.kwargs["username"]
        )
        return self.profile_user.followers.all()

    def get_context_data(self, **kwargs):
        """
        Add profile user to context.
        """
        context = super().get_context_data(**kwargs)
        context["users"] = self.profile_user
        return context


class CustomUserFollowingListView(ListView):
    """
    Display a list of users who follow the desired user.
    """
    model = CustomUser
    template_name = "accounts/users.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        """
        Return following of the target user.
        """
        self.profile_user = get_object_or_404(
            CustomUser, username=self.kwargs["username"]
        )
        return self.profile_user.following.all()

    def get_context_data(self, **kwargs):
        """
        Add profile user to context.
        """
        context = super().get_context_data(**kwargs)
        context["users"] = self.profile_user
        return context
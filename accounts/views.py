from typing import Any

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from tweets.models import Tweet

from .forms import SignupForm
from .models import User


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserProfileView(ListView):
    model = User
    template_name = "accounts/user_profile.html"
    slug_field = "username"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs["username"])
        context["user_profile"] = user
        context["tweets"] = Tweet.objects.filter(author=user)
        return context

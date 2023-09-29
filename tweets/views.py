# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

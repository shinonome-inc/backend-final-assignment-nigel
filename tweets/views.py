from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .models import Tweet


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "tweets/home.html"

    def get_queryset(self):
        return Tweet.objects.select_related("author").order_by("-created_at")


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    template_name = "tweets/create.html"
    success_url = reverse_lazy("tweets:home")
    fields = ["text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = "tweets/tweet_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return Tweet.objects.get(id=self.kwargs["pk"])


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy("tweets:home")
    template = "tweets/tweet_confirm_delete.html"

    def test_func(self):
        tweet = self.get_object()
        return tweet.author == self.request.user

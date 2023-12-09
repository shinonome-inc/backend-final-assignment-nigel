import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:home")
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")

    def test_success_get(self):
        [Tweet.objects.create(text=f"test{i}", author=self.user) for i in range(0, 5)]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")
        self.assertQuerysetEqual(Tweet.objects.all().order_by("-created_at"), response.context["tweet_list"])


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        self.url = reverse("tweets:create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        valid_data = {"text": "Testing123", "author": self.user}
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)
        self.assertTrue(Tweet.objects.filter(text=valid_data["text"]).exists())

    def test_failure_post_with_empty_content(self):
        invalid_data = {"text": "", "author": self.user}
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("This field is required.", form.errors["text"])
        self.assertFalse(Tweet.objects.filter(text=invalid_data["text"]).exists())

    def test_failure_post_with_too_long_content(self):
        invalid_data = {
            "text": "".join(random.choice("abcdefgh") for _ in range(281)),
            "author": self.user,
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn(
            f"Ensure this value has at most 280 characters (it has {len(invalid_data['text'])}).", form.errors["text"]
        )
        self.assertFalse(Tweet.objects.filter(text=invalid_data["text"]).exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        samples = [Tweet.objects.create(text=f"test{i}", author=self.user) for i in range(0, 5)]
        self.test_id = samples[0].id
        self.test_url = reverse("tweets:detail", args=[self.test_id])

    def test_success_get(self):
        response = self.client.get(self.test_url)
        self.assertEqual(Tweet.objects.get(id=self.test_id), response.context["tweet"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        samples = [Tweet.objects.create(text=f"test{i}", author=self.user) for i in range(0, 5)]
        self.test_id = samples[0].id
        self.url = reverse("tweets:delete", args=[self.test_id])

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)
        self.assertFalse(Tweet.objects.filter(id=self.test_id).exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:delete", args=[10]))
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Tweet.objects.filter(id=10).exists())

    def test_failure_post_with_incorrect_user(self):
        User.objects.create_user(username="tester2", password="testpassword")
        self.client.login(username="tester2", password="testpassword")
        response = self.client.post(reverse("tweets:delete", args=[self.test_id]))
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Tweet.objects.filter(id=10).exists())


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):

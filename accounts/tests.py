from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL), status_code=302, target_status_code=200)
        self.assertTrue(User.objects.filter(username=valid_data["username"]).exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        invalid_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["username"])
        self.assertIn("This field is required.", form.errors["email"])
        self.assertIn("This field is required.", form.errors["password1"])
        self.assertIn("This field is required.", form.errors["password2"])

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["username"])

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "username",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["email"])

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "username",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["password1"])

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["email"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_failure_post_with_duplicated_user(self):
        self.user = User.objects.create_user(username="tster", password="testpassword")
        invalid_data = {
            "username": "tster",
            "email": "test@test.com",
            "password1": "1234p",
            "password2": "1234p",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("A user with that username already exists.", form.errors["username"])

    def test_failure_post_with_too_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "1234p",
            "password2": "1234p",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("This password is too short. It must contain at least 8 characters.", form.errors["password2"])

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testuser123",
            "password2": "testuser123",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("The password is too similar to the username.", form.errors["password2"])

    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("This password is entirely numeric.", form.errors["password2"])

    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassward",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("The two password fields didn’t match.", form.errors["password2"])


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        valid_data = {
            "username": "tester",
            "password": "testpassword",
        }
        response = self.client.post(self.url, valid_data)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        invalid_data = {
            "username": "test",
            "password": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertIn(
            "Please enter a correct username and password. Note that both fields may be case-sensitive.",
            form.errors["__all__"],
        )

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "tester",
            "password": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertIn(
            "This field is required.",
            form.errors["password"],
        )


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")

    def test_success_post(self):
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL), status_code=302, target_status_code=200)
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        self.url = reverse("accounts:user_profile", args=[self.user])

    def test_success_get(self):
        [Tweet.objects.create(text=f"test{i}", author=self.user) for i in range(1, 5)]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/user_profile.html")
        self.assertQuerysetEqual(Tweet.objects.filter(author=self.user), response.context["tweets"], ordered=False)


# class TestUserProfileEditView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_not_exists_user(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestFollowView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_user(self):

#     def test_failure_post_with_self(self):


# class TestUnfollowView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestFollowingListView(TestCase):
#     def test_success_get(self):


# class TestFollowerListView(TestCase):
#     def test_success_get(self):

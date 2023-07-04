from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

# Create your tests here.


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )

        cls.post = Post.objects.create(
            title="A good title",
            body="Nice body content",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "A good title")
        self.assertEqual(self.post.body, "Nice body content")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "A good title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/post/1/").status_code, 200)
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "A good title")

    def test_post_detailview(self):
        response = self.client.get(
            reverse(
                "post_detail",
                kwargs={"pk": self.post.pk},
            )
        )
        self.assertTemplateUsed(response, "post_detail.html")
        self.assertContains(response, "Nice body content")

    def test_post_createview(self):
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "New title",
                "body": "New text",
                "author": self.user.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.objects.last().body, "New text")

    def test_post_updateview(self):
        response = self.client.post(
            reverse("post_edit", kwargs={"pk": "1"}),
            {
                "title": "Edited title",
                "body": "Edited content",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Edited title")
        self.assertEqual(Post.objects.last().body, "Edited content")

    def test_post_deleteview(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)

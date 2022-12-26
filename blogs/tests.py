from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Blog, Category


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="test_user",
            email="test_user@email.com",
            password="test_user_password",
        )
        cls.category = Category.objects.create(category_name="Python")
        cls.blog = Blog.objects.create(
            author=cls.user,
            blog_title="Intermediate Python",
            blog_category=cls.category,
            blog_body="Some text about python",
        )

    def test_blog_listing(self):
        self.assertEqual(self.blog.author, self.user)
        self.assertEqual(self.blog.blog_title, "Intermediate Python")
        self.assertEqual(self.blog.blog_category, self.category)
        self.assertEqual(self.blog.blog_body, "Some text about python")

    def test_home_page_view(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Intermediate Python")
        self.assertTemplateUsed(response, "blogs/home.html")

    def test_blogs_detail_view(self):
        response = self.client.get(self.blog.get_absolute_url())
        no_response = self.client.get("/blogs/99999/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Intermediate Python")
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")

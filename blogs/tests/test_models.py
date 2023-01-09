from django.test import TestCase
from django.contrib.auth import get_user_model
from blogs.models import Blog, Category


class CategoryModelTests(TestCase):
    def test_category_model(self):
        category = Category.objects.create(category_name="Writing tests")

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().category_name, "Writing tests")
        self.assertEqual(str(category), "Writing tests")


class BlogModelTests(TestCase):
    def setUp(self):
        # Creating user
        User = get_user_model()
        self.user = User.objects.create_user(
            email="test_user@email.com",
            username="test_user",
            password="test_user_password",
        )

        # Creating category
        self.category = Category.objects.create(category_name="Writing tests")

        # Creating blog
        self.blog = Blog.objects.create(
            author=self.user,
            blog_title="Test blog",
            blog_category=self.category,
            blog_body="This is a test blog.",
        )

    def test_blog_model(self):
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.first().blog_title, "Test blog")
        self.assertEqual(str(self.blog), "Test blog")
        self.assertEqual(self.blog.get_absolute_url(), f"/blog/{self.blog.id}/")

        self.assertEqual(Blog.published_objects.count(), 1)
        self.blog.blog_status = "draft"
        self.blog.save()
        self.assertEqual(Blog.published_objects.count(), 0)
        self.assertEqual(Blog.objects.count(), 1)

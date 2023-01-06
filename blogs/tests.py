from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Blog, Category


class BlogHomeAndDetailPageTests(TestCase):
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
        self.assertEqual(self.blog.blog_category.category_name, "Python")
        self.assertEqual(self.blog.blog_body, "Some text about python")

    def test_home_page_view(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_blogs_detail_view(self):
        response = self.client.get(self.blog.get_absolute_url())
        no_response = self.client.get("/blogs/99999/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Intermediate Python")
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")


class BlogCreateUpdateDeleteTests(TestCase):
    def setUp(self):
        # For CreateBlogView
        self.category1 = Category.objects.create(category_name="Test Category number 1")
        # For UpdateBlogView and DeleteBlogView
        self.category2 = Category.objects.create(category_name="Test Category number 2")

        User = get_user_model()
        self.user = User.objects.create_user(
            email="testuser@email.com", username="testuser", password="testpass"
        )
        self.client.login(email="testuser@email.com", password="testpass")

        self.blog_for_update_and_delete_views = Blog.objects.create(
            author=self.user,
            blog_title="Test Blog",
            blog_category=self.category1,
            blog_body="This is a test blog.",
        )

    def test_create_blog_view_for_get_request(self):
        response = self.client.get(reverse("create_blog"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create blog")
        self.assertTemplateUsed(response, "blogs/create_blog.html")

    def test_create_blog_view_for_post_request(self):
        form_data = {
            "blog_title": "Test Blog",
            "blog_category": self.category1.pk,
            "blog_body": "This is a test blog.",
        }

        response = self.client.post(reverse("create_blog"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 2)

        new_blog = Blog.objects.last()
        self.assertEqual(new_blog.blog_title, "Test Blog")
        self.assertEqual(new_blog.blog_category.category_name, "Test Category number 1")
        self.assertEqual(new_blog.blog_body, "This is a test blog.")
        self.assertEqual(new_blog.author.username, self.user.username)

    def test_update_blog_view_for_get_request(self):
        response = self.client.get(
            reverse(
                "update_blog", kwargs={"pk": self.blog_for_update_and_delete_views.pk}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update blog")
        self.assertTemplateUsed(response, "blogs/update_blog.html")

    def test_update_blog_view_for_post_request(self):
        update_form_data = {
            "blog_title": "Updated Test Blog",
            "blog_category": self.category2.pk,
            "blog_body": "This is an updated test blog.",
        }

        response = self.client.post(
            reverse(
                "update_blog", kwargs={"pk": self.blog_for_update_and_delete_views.pk}
            ),
            data=update_form_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 1)

        updated_blog = Blog.objects.last()
        self.assertEqual(updated_blog.blog_title, "Updated Test Blog")
        self.assertEqual(
            updated_blog.blog_category.category_name, "Test Category number 2"
        )
        self.assertEqual(updated_blog.blog_body, "This is an updated test blog.")
        self.assertEqual(updated_blog.author.username, self.user.username)

    def test_delete_blog_view_for_get_request(self):
        response = self.client.get(
            reverse(
                "delete_blog", kwargs={"pk": self.blog_for_update_and_delete_views.pk}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete blog")
        self.assertTemplateUsed(response, "blogs/delete_blog.html")

    def test_delete_blog_view_for_post_request(self):
        response = self.client.post(
            reverse(
                "delete_blog", kwargs={"pk": self.blog_for_update_and_delete_views.pk}
            )
        )
        no_response = self.client.get(
            reverse(
                "delete_blog", kwargs={"pk": self.blog_for_update_and_delete_views.pk}
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(no_response.status_code, 404)
        self.assertEqual(Blog.objects.count(), 0)


class ContactPageTest(TestCase):
    """
    Test class created for testing contact form
    and contact page view
    """

    def setUp(self):
        self.subject = "Testing email"
        self.body = "This is going to be a test for my contact form that sends emails from users to me."
        self.email_from = "test_user_1"
        self.email_to = "test_user_2"
        self.reply_to = self.email_from

    def test_sending_email(self):
        mail.EmailMessage(
            self.subject,
            self.body,
            self.email_from,
            [self.email_to],
            reply_to=[self.email_to],
        ).send()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Testing email")

    def test_contact_page_view(self):
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)
        # one of the input fields in contact form
        self.assertContains(response, "Your Email")
        self.assertTemplateUsed(response, "blogs/contact_form.html")

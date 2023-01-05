from django.core import mail
from django.test import TestCase
from django.contrib.auth import get_user_model
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
        self.assertTemplateUsed(response, "home.html")

    def test_blogs_detail_view(self):
        response = self.client.get(self.blog.get_absolute_url())
        no_response = self.client.get("/blogs/99999/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Intermediate Python")
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")


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

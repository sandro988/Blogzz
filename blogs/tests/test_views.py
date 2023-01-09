from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from blogs.models import Blog, Category


class TestsData:
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.client = Client()
        cls.user = User.objects.create_user(
            email="test_user@email.com",
            username="test_user",
            password="test_user_password",
        )

        cls.category1 = Category.objects.create(category_name="Python")

        cls.blog = Blog.objects.create(
            author=cls.user,
            blog_title="Intermediate Python",
            blog_category=cls.category1,
            blog_body="Some text about python",
        )


class HomePageViewTest(TestsData, TestCase):
    def test_blog_listing(self):
        self.assertEqual(self.blog.author, self.user)
        self.assertEqual(self.blog.blog_title, "Intermediate Python")
        self.assertEqual(self.blog.blog_category.category_name, "Python")
        self.assertEqual(self.blog.blog_body, "Some text about python")

    def test_home_page_view(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class BlogDetailViewTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_blogs_detail_view(self):
        """
        Test case where a logged in user tries to access individual blog post.
        """
        response = self.client.get(self.blog.get_absolute_url())
        no_response = self.client.get("/blogs/99999/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Intermediate Python")
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")

    def test_blogs_detail_view_for_logged_out_user(self):
        """
        Test case where a logged out user tries to access individual blog post.
        """

        self.client.logout()
        response = self.client.get(self.blog.get_absolute_url())
        no_response = self.client.get("/blogs/99999/")

        # User tries to access the page without being authenticated
        self.assertEqual(response.status_code, 302)
        self.assertEqual(no_response.status_code, 404)
        self.assertRedirects(
            response,
            f"%s?next={self.blog.get_absolute_url()}" % (reverse("account_login")),
        )

        # User gets redirected to login page
        response = self.client.get(
            f"%s?next={self.blog.get_absolute_url()}" % (reverse("account_login"))
        )
        self.assertContains(response, "Welcome back")
        self.assertTemplateUsed(response, "account/login.html")


class CreateBlogViewTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_create_blog_view(self):
        response = self.client.get(reverse("create_blog"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create blog")
        self.assertTemplateUsed(response, "blogs/create_blog.html")

    def test_create_blog_view_for_logged_out_user(self):

        self.client.logout()
        response = self.client.get(reverse("create_blog"))

        # User tries to access the create page without being authenticated
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={reverse('create_blog')}"
        )

        # User gets redirected to login page
        response = self.client.get(
            f"{reverse('account_login')}?next={reverse('create_blog')}"
        )
        self.assertContains(response, "Welcome back")
        self.assertTemplateUsed(response, "account/login.html")


class UpdateBlogViewTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

        # Another user that will be used in test_update_blog_view_when_user_is_not_author test, to check
        # how the view behaves when a non author user tries to update a blog.
        User = get_user_model()
        User.objects.create_user(
            email="not_an_author_user@email.com",
            username="not_an_author_user",
            password="not_an_author_user_password",
        )

    def test_update_blog_view(self):
        response = self.client.get(reverse("update_blog", kwargs={"pk": self.blog.pk}))
        pk_invalid = self.client.get("update_blog/123456/")
        pk_does_not_exist = self.client.get(
            "/update_blog/00000000-0000-0000-0000-000000000000/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)
        self.assertContains(response, "Update blog")
        self.assertTemplateUsed(response, "blogs/update_blog.html")

    def test_update_blog_view_for_logged_out_user(self):
        self.client.logout()
        update_page_url = reverse("update_blog", kwargs={"pk": self.blog.pk})

        response = self.client.get(update_page_url)

        # User tries to access the update page without being authenticated
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={update_page_url}"
        )

        # User gets redirect to login page
        response = self.client.get(f"{reverse('account_login')}?next={update_page_url}")
        self.assertContains(response, "Welcome back")
        self.assertTemplateUsed(response, "account/login.html")

    def test_update_blog_view_when_user_is_not_author(self):
        self.client.logout()
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )

        response = self.client.get(reverse("update_blog", kwargs={"pk": self.blog.pk}))

        self.assertEqual(response.status_code, 403)


class DeleteBlogViewTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        User = get_user_model()
        User.objects.create_user(
            email="not_an_author_user@email.com",
            username="not_an_author_user",
            password="not_an_author_user_password",
        )

    def test_delete_blog_view(self):
        response = self.client.get(reverse("delete_blog", kwargs={"pk": self.blog.pk}))
        pk_invalid = self.client.get("delete_blog/123456/")
        pk_does_not_exist = self.client.get(
            "/delete_blog/00000000-0000-0000-0000-000000000000/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)
        self.assertContains(response, "Delete blog")
        self.assertTemplateUsed(response, "blogs/delete_blog.html")

    def test_delete_blog_view_for_logged_out_user(self):
        self.client.logout()
        delete_page_url = reverse("delete_blog", kwargs={"pk": self.blog.pk})

        response = self.client.get(delete_page_url)

        # User tries to access the delete page without being authenticated
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={delete_page_url}"
        )

        # User gets redirect to login page
        response = self.client.get(f"{reverse('account_login')}?next={delete_page_url}")
        self.assertContains(response, "Welcome back")
        self.assertTemplateUsed(response, "account/login.html")

    def test_delete_blog_view_when_user_is_not_author(self):
        self.client.logout()
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )

        response = self.client.get(reverse("delete_blog", kwargs={"pk": self.blog.pk}))
        self.assertEqual(response.status_code, 403)


class ContactPageViewTests(TestCase):
    def test_contact_page_view(self):
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)
        # one of the input fields in contact form
        self.assertContains(response, "Your Email")
        self.assertTemplateUsed(response, "blogs/contact_form.html")

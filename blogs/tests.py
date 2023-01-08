from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Blog, Category


class BlogTestsData:
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
        # For CreateBlogView
        cls.category2 = Category.objects.create(
            category_name="Category for Create view"
        )
        # For UpdateBlogView and DeleteBlogView
        cls.category3 = Category.objects.create(
            category_name="Category for Create and Update views"
        )

        # This blog will be used in tests for Detail, Update, Delete views.
        cls.blog = Blog.objects.create(
            author=cls.user,
            blog_title="Intermediate Python",
            blog_category=cls.category1,
            blog_body="Some text about python",
        )


class HomePageViewTests(BlogTestsData, TestCase):
    def test_blog_listing(self):
        self.assertEqual(self.blog.author, self.user)
        self.assertEqual(self.blog.blog_title, "Intermediate Python")
        self.assertEqual(self.blog.blog_category.category_name, "Python")
        self.assertEqual(self.blog.blog_body, "Some text about python")

    def test_home_page_view(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class DetailPageViewTests(BlogTestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_blogs_detail_view(self):
        """
        Test case where a logged in user tries to access individual blog posts.
        """
        response = self.client.get(self.blog.get_absolute_url())
        no_response = self.client.get("/blogs/99999/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Intermediate Python")
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")

    def test_blogs_detail_view_for_logged_out_user(self):
        """
        Test case where a logged out user tries to access individual blog posts.
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


class CreateBlogPageViewTests(BlogTestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_create_blog_view_for_get_request(self):
        response = self.client.get(reverse("create_blog"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create blog")
        self.assertTemplateUsed(response, "blogs/create_blog.html")

    def test_create_blog_view_for_post_request(self):
        form_data = {
            "blog_title": "Test Blog",
            "blog_category": self.category2.pk,
            "blog_body": "This is a test blog.",
        }

        response = self.client.post(reverse("create_blog"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 2)

        new_blog = Blog.objects.get(blog_title="Test Blog")
        self.assertEqual(new_blog.blog_title, "Test Blog")
        self.assertEqual(
            new_blog.blog_category.category_name, "Category for Create view"
        )
        self.assertEqual(new_blog.blog_body, "This is a test blog.")
        self.assertEqual(new_blog.author.username, self.user.username)

    def test_create_blog_view_for_post_request_with_create_button(self):
        form_data = {
            "blog_title": "Test Blog",
            "blog_category": self.category2.pk,
            "blog_body": "This is a test blog.",
            "Create": "Create",
        }

        response = self.client.post(reverse("create_blog"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 2)

        new_blog = Blog.objects.get(blog_title="Test Blog")
        self.assertEqual(new_blog.blog_title, "Test Blog")
        self.assertEqual(
            new_blog.blog_category.category_name, "Category for Create view"
        )
        self.assertEqual(new_blog.blog_body, "This is a test blog.")
        self.assertEqual(new_blog.blog_status, "published")
        self.assertEqual(new_blog.author.username, self.user.username)

    def test_create_blog_view_for_post_request_with_move_to_drafts_button(self):
        form_data = {
            "blog_title": "Test Blog",
            "blog_category": self.category2.pk,
            "blog_body": "This is a test blog.",
            "Move to drafts": "Move to drafts",
        }

        response = self.client.post(reverse("create_blog"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 2)

        new_blog = Blog.objects.get(blog_title="Test Blog")
        self.assertEqual(new_blog.blog_title, "Test Blog")
        self.assertEqual(
            new_blog.blog_category.category_name, "Category for Create view"
        )
        self.assertEqual(new_blog.blog_body, "This is a test blog.")
        self.assertEqual(new_blog.blog_status, "draft")
        self.assertEqual(new_blog.author.username, self.user.username)

    def test_create_blog_view_with_incomplete_form_data(self):
        form_data = {
            "blog_title": "",
            "blog_category": self.category2.pk,
            "blog_body": "This is a test blog.",
        }

        response = self.client.post(reverse("create_blog"), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            form="form",
            field="blog_title",
            errors=["This field is required."],
            msg_prefix="Error: ",
        )
        self.assertContains(response, "Create blog")
        self.assertContains(response, "This field is required")
        self.assertTemplateUsed(response, "blogs/create_blog.html")
        # Checking that no new blog has been created
        self.assertEqual(Blog.objects.count(), 1)

    def test_create_blog_view_for_logged_out_user(self):
        """Test case where a logged out user tries to go to a create blog page and create a new blog post"""

        self.client.logout()

        def request_method_GET():
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

        def request_method_POST():
            form_data = {
                "blog_title": "Test Blog",
                "blog_category": self.category2.pk,
                "blog_body": "This is a test blog.",
            }

            response = self.client.post(reverse("create_blog"), data=form_data)

            # User tries to access the create page without being authenticated
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Blog.objects.count(), 1)
            self.assertNotEqual(Blog.objects.last().blog_title, "Test Blog")
            self.assertRedirects(
                response, f"{reverse('account_login')}?next={reverse('create_blog')}"
            )

            # User gets redirect to login page
            response = self.client.get(
                f"{reverse('account_login')}?next={reverse('create_blog')}"
            )
            self.assertContains(response, "Welcome back")
            self.assertTemplateUsed(response, "account/login.html")

        request_method_GET()
        request_method_POST()


class UpdateBlogPageViewTests(BlogTestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_update_blog_view_for_get_request(self):
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

    def test_update_blog_view_for_post_request(self):
        update_form_data = {
            "blog_title": "Updated Test Blog",
            "blog_category": self.category3.pk,
            "blog_body": "This is an updated test blog.",
        }

        response = self.client.post(
            reverse("update_blog", kwargs={"pk": self.blog.pk}),
            data=update_form_data,
        )
        pk_invalid = self.client.post("update_blog/123456/", data=update_form_data)
        pk_does_not_exist = self.client.post(
            "/update_blog/00000000-0000-0000-0000-000000000000/", data=update_form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)
        self.assertEqual(Blog.objects.count(), 1)

        updated_blog = Blog.objects.last()
        self.assertEqual(updated_blog.blog_title, "Updated Test Blog")
        self.assertEqual(
            updated_blog.blog_category.category_name,
            "Category for Create and Update views",
        )
        self.assertEqual(updated_blog.blog_body, "This is an updated test blog.")
        self.assertEqual(updated_blog.author.username, self.user.username)

    def test_update_blog_view_for_post_request_with_move_to_drafts_button(self):

        """
        A test case when a user wants to update the blog and move it from published blog to drafts.
        """

        update_form_data = {
            "blog_title": "Updated Test Blog",
            "blog_category": self.category3.pk,
            "blog_body": "This is an updated test blog.",
            "Move to drafts": "Move to drafts",
        }

        response = self.client.post(
            reverse("update_blog", kwargs={"pk": self.blog.pk}),
            data=update_form_data,
        )
        pk_invalid = self.client.post("update_blog/123456/", data=update_form_data)
        pk_does_not_exist = self.client.post(
            "/update_blog/00000000-0000-0000-0000-000000000000/", data=update_form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)
        self.assertEqual(Blog.objects.count(), 1)

        updated_blog = Blog.objects.last()
        self.assertEqual(updated_blog.blog_title, "Updated Test Blog")
        self.assertEqual(
            updated_blog.blog_category.category_name,
            "Category for Create and Update views",
        )
        self.assertEqual(updated_blog.blog_body, "This is an updated test blog.")
        self.assertEqual(updated_blog.blog_status, "draft")
        self.assertEqual(updated_blog.author.username, self.user.username)

    def test_update_blog_view_for_post_request_with_publish_button(self):

        """
        A test case when a user wants to move update their blog with the status of 'draft' and also change its status to
        'published', so that this blog appears on the home page.
        """

        update_form_data = {
            "blog_title": "Updated Test Blog",
            "blog_category": self.category3.pk,
            "blog_body": "This is an updated test blog.",
            "Publish": "Publish",
        }

        response = self.client.post(
            reverse("update_blog", kwargs={"pk": self.blog.pk}),
            data=update_form_data,
        )
        pk_invalid = self.client.post("update_blog/123456/", data=update_form_data)
        pk_does_not_exist = self.client.post(
            "/update_blog/00000000-0000-0000-0000-000000000000/", data=update_form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)
        self.assertEqual(Blog.objects.count(), 1)

        updated_blog = Blog.objects.last()
        self.assertEqual(updated_blog.blog_title, "Updated Test Blog")
        self.assertEqual(
            updated_blog.blog_category.category_name,
            "Category for Create and Update views",
        )
        self.assertEqual(updated_blog.blog_body, "This is an updated test blog.")
        self.assertEqual(updated_blog.blog_status, "published")
        self.assertEqual(updated_blog.author.username, self.user.username)

    def test_update_blog_view_for_logged_out_user(self):
        """Test case where a logged out user tries to go to an update blog page and update an already existing blog post"""

        self.client.logout()
        update_page_url = reverse("update_blog", kwargs={"pk": self.blog.pk})

        def request_method_GET():
            response = self.client.get(update_page_url)

            # User tries to access the update page without being authenticated
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(
                response, f"{reverse('account_login')}?next={update_page_url}"
            )

            # User gets redirect to login page
            response = self.client.get(
                f"{reverse('account_login')}?next={update_page_url}"
            )
            self.assertContains(response, "Welcome back")
            self.assertTemplateUsed(response, "account/login.html")

        def request_method_POST():
            update_form_data = {
                "blog_title": "Test Blog Update",
                "blog_category": self.category3.pk,
                "blog_body": "This is a test blog.",
            }

            response = self.client.post(update_page_url, data=update_form_data)

            # User tries to access the update page without being authenticated
            self.assertEqual(response.status_code, 302)
            self.assertNotEqual(Blog.objects.last().blog_title, "Test Blog Update")
            self.assertRedirects(
                response, f"{reverse('account_login')}?next={update_page_url}"
            )

            # User gets redirected to login page
            response = self.client.get(
                f"{reverse('account_login')}?next={update_page_url}"
            )
            self.assertContains(response, "Welcome back")
            self.assertTemplateUsed(response, "account/login.html")

        request_method_GET()
        request_method_POST()

    def test_update_blog_view_with_incomplete_form_data(self):
        update_form_data = {
            "blog_title": "",
            "blog_category": self.category3.pk,
            "blog_body": "This is a test blog.",
        }

        update_page_url = reverse("update_blog", kwargs={"pk": self.blog.pk})
        response = self.client.post(update_page_url, data=update_form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            form="form",
            field="blog_title",
            errors=["This field is required."],
            msg_prefix="Error: ",
        )
        self.assertContains(response, "Update blog")
        self.assertContains(response, "This field is required")
        self.assertTemplateUsed(response, "blogs/update_blog.html")
        # Checking that the blog has not changed
        self.assertNotEqual(Blog.objects.last().blog_title, "")

    def test_update_blog_view_when_user_is_not_author(self):
        """
        Test where a non-author user is redirected to the "permission denied" page
        when they try to update a blog post.
        """

        User = get_user_model()
        new_user = User.objects.create_user(
            email="new_test_user@email.com",
            username="new_test_user",
            password="new_test_user_password",
        )
        self.client.logout()
        self.client.login(
            email="new_test_user@email.com", password="new_test_user_password"
        )

        updated_form_data = {
            "blog_title": "I am not author of this post",
            "blog_category": self.category3.pk,
            "blog_body": "This is a test blog that has been updated.",
        }

        def request_method_GET():
            response = self.client.get(
                reverse("update_blog", kwargs={"pk": self.blog.pk})
            )

            self.assertEqual(response.status_code, 403)

        def request_method_POST():
            response = self.client.post(
                reverse("update_blog", kwargs={"pk": self.blog.pk}),
                data=updated_form_data,
            )

            self.assertEqual(response.status_code, 403)
            self.assertNotEqual(
                Blog.objects.last().blog_title, "I am not author of this post"
            )
            self.assertNotEqual(
                Blog.objects.last().author.username, User.objects.last().username
            )

        request_method_GET()
        request_method_POST()


class DeleteBlogPageViewTests(BlogTestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_delete_blog_view_for_get_request(self):
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

    def test_delete_blog_view_for_post_request(self):
        response = self.client.post(reverse("delete_blog", kwargs={"pk": self.blog.pk}))
        no_response = self.client.get(
            reverse("delete_blog", kwargs={"pk": self.blog.pk})
        )
        pk_invalid = self.client.post("delete_blog/123456/")
        pk_does_not_exist = self.client.post(
            "/delete_blog/00000000-0000-0000-0000-000000000000/"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(no_response.status_code, 404)
        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)
        self.assertEqual(Blog.objects.count(), 0)

    def test_delete_blog_view_for_logged_out_user(self):
        self.client.logout()
        delete_page_url = reverse("delete_blog", kwargs={"pk": self.blog.pk})

        def request_method_GET():
            response = self.client.get(delete_page_url)

            # User tries to access the delete page without being authenticated
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(
                response, f"{reverse('account_login')}?next={delete_page_url}"
            )

            # User gets redirect to login page
            response = self.client.get(
                f"{reverse('account_login')}?next={delete_page_url}"
            )
            self.assertContains(response, "Welcome back")
            self.assertTemplateUsed(response, "account/login.html")

        def request_method_POST():
            response = self.client.post(delete_page_url)

            # User tries to access the delete page without being authenticated
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Blog.objects.last().blog_title, "Intermediate Python")
            self.assertRedirects(
                response, f"{reverse('account_login')}?next={delete_page_url}"
            )

            # User gets redirected to login page
            response = self.client.get(
                f"{reverse('account_login')}?next={delete_page_url}"
            )
            self.assertContains(response, "Welcome back")
            self.assertTemplateUsed(response, "account/login.html")

        request_method_GET()
        request_method_POST()

    def test_delete_blog_view_when_user_is_not_author(self):
        """
        Test where a non-author user is redirected to the "permission denied" page
        when they try to delete a blog post.
        """

        User = get_user_model()
        new_user = User.objects.create_user(
            email="new_test_user@email.com",
            username="new_test_user",
            password="new_test_user_password",
        )
        self.client.logout()
        self.client.login(
            email="new_test_user@email.com", password="new_test_user_password"
        )

        def request_method_GET():
            response = self.client.get(
                reverse("delete_blog", kwargs={"pk": self.blog.pk})
            )

            self.assertEqual(response.status_code, 403)

        def request_method_POST():
            response = self.client.post(
                reverse("delete_blog", kwargs={"pk": self.blog.pk}),
            )

            self.assertEqual(response.status_code, 403)
            self.assertEqual(Blog.objects.count(), 1)
            self.assertEqual(Blog.objects.last().blog_title, "Intermediate Python")

        request_method_GET()
        request_method_POST()


class ContactPageTests(TestCase):
    """
    Test class created for testing contact form
    and contact page view
    """

    @classmethod
    def setUpTestData(cls):
        cls.subject = "Testing email"
        cls.body = "This is going to be a test for my contact form that sends emails from users to me."
        cls.email_from = "test_user_1"
        cls.email_to = "test_user_2"
        cls.reply_to = cls.email_from

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

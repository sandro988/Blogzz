from django.core import mail
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

        cls.category1 = "Python"
        # For CreateBlogView
        cls.category2 = "Category for Create view"
        # For UpdateBlogView and DeleteBlogView
        cls.category3 = "Category for Create and Update views"

        cls.blog = Blog.objects.create(
            author=cls.user,
            blog_title="Intermediate Python",
            blog_category=cls.category1,
            blog_body="Some text about python",
        )


class SearchBlogFormTests(TestsData, TestCase):
    def test_searching_functionality(self):
        response = self.client.get(reverse("home"), {"q": "Python"})

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["blog_list"], [self.blog])

    def test_search_value_does_not_exist(self):
        response = self.client.get(reverse("home"), {"q": "1234567890"})

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["blog_list"], [self.blog])


class CreateBlogViewFormTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        self.form_data = {
            "blog_title": "Test Blog",
            "blog_category": self.category1,
            "blog_body": "This is a test blog.",
            # Simulating that user clicked Create button instead of Move to drafts.
            "Create": "Create",
        }

        self.incomplete_form_data = {
            "blog_title": "",
            "blog_category": self.category1,
            "blog_body": "This is a test blog.",
            # Simulating that user clicked Create button instead of Move to drafts.
            "Create": "Create",
        }

    def test_create_blog_form_with_valid_data(self):
        response = self.client.post(reverse("create_blog"), data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 2)

        new_blog = Blog.objects.get(blog_title="Test Blog")
        self.assertEqual(new_blog.blog_title, "Test Blog")
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(
            new_blog.blog_category_foreignkey.category_name, self.category1
        )
        self.assertEqual(new_blog.blog_body, "This is a test blog.")
        self.assertEqual(new_blog.blog_status, "published")
        self.assertEqual(new_blog.author.username, self.user.username)

    def test_create_blog_form_with_incomplete_data(self):
        response = self.client.post(
            reverse("create_blog"), data=self.incomplete_form_data
        )

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

    def test_create_blog_form_for_logged_out_user(self):
        self.client.logout()

        response = self.client.post(reverse("create_blog"), data=self.form_data)

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

    def test_create_blog_form_with_move_to_drafts_button_clicked(self):

        """
        Test case for a scenario where, user saves the blog as a draft instead of publishing it.
        """

        self.form_data.pop("Create")
        self.form_data["Move to drafts"] = "Move to drafts"

        response = self.client.post(reverse("create_blog"), data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 2)

        new_blog = Blog.objects.get(blog_title="Test Blog")
        self.assertEqual(new_blog.blog_title, "Test Blog")
        self.assertEqual(
            new_blog.blog_category_foreignkey.category_name, self.category1
        )
        self.assertEqual(new_blog.blog_body, "This is a test blog.")
        self.assertEqual(new_blog.blog_status, "draft")
        self.assertEqual(new_blog.author.username, self.user.username)


class UpdateBlogViewFormTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        self.update_form_data = {
            "blog_title": "Updated Test Blog",
            "blog_category": self.category3,
            "blog_body": "This is an updated test blog.",
        }
        self.update_form_data_of_nonauthor_user = {
            "blog_title": "I am not author of this post",
            "blog_category": self.category3,
            "blog_body": "This is a test blog that has been updated.",
        }
        self.incomplete_update_form_data = {
            "blog_title": "",
            "blog_category": self.category3,
            "blog_body": "This is a test blog.",
        }

        # Creating non author user
        self.User = get_user_model()
        self.User.objects.create_user(
            email="not_an_author_user@email.com",
            username="not_an_author_user",
            password="not_an_author_user_password",
        )

    def test_update_blog_form_with_valid_data(self):
        response = self.client.post(
            reverse("update_blog", kwargs={"pk": self.blog.pk}),
            data=self.update_form_data,
        )
        pk_invalid = self.client.post("update_blog", kwargs={"pk": "123456"})
        pk_does_not_exist = self.client.post(
            "update_blog", kwargs={"pk": "00000000-0000-0000-0000-000000000000/"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)
        self.assertEqual(Blog.objects.count(), 1)

        updated_blog = Blog.objects.last()
        self.assertEqual(updated_blog.blog_title, "Updated Test Blog")
        # In the view we use title() method, so the catgory name will have first letters of each word as uppercase.
        self.assertEqual(
            updated_blog.blog_category_foreignkey.category_name,
            "Category For Create And Update Views",
        )
        self.assertEqual(updated_blog.blog_body, "This is an updated test blog.")
        self.assertEqual(updated_blog.blog_status, "published")
        self.assertEqual(updated_blog.author.username, self.user.username)

    def test_update_blog_form_with_incomplete_data(self):
        update_page_url = reverse("update_blog", kwargs={"pk": self.blog.pk})
        response = self.client.post(
            update_page_url, data=self.incomplete_update_form_data
        )

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

    def test_update_blog_form_for_logged_out_user(self):
        self.client.logout()
        update_page_url = reverse("update_blog", kwargs={"pk": self.blog.pk})
        response = self.client.post(update_page_url, data=self.update_form_data)

        # User tries to access the update page without being authenticated
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(Blog.objects.last().blog_title, "Test Blog Update")
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={update_page_url}"
        )

        # User gets redirected to login page
        response = self.client.get(f"{reverse('account_login')}?next={update_page_url}")
        self.assertContains(response, "Welcome back")
        self.assertTemplateUsed(response, "account/login.html")

    def test_update_blog_form_when_user_is_not_author(self):
        self.client.logout()
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )

        response = self.client.post(
            reverse("update_blog", kwargs={"pk": self.blog.pk}),
            data=self.update_form_data_of_nonauthor_user,
        )

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(
            Blog.objects.last().blog_title, "I am not author of this post"
        )
        self.assertNotEqual(
            Blog.objects.last().author.username, self.User.objects.last().username
        )

    def test_update_blog_form_with_move_to_drafts_button_clicked(self):

        """
        Test for a scenario where a blog is published, but user updates it and moves it to drafts.
        """

        self.update_form_data["Move to drafts"] = "Move to drafts"

        response = self.client.post(
            reverse("update_blog", kwargs={"pk": self.blog.pk}),
            data=self.update_form_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 1)

        updated_blog = Blog.objects.last()
        self.assertEqual(updated_blog.blog_title, "Updated Test Blog")

        # In the view we use title() method, so the catgory name will have first letters of each word as uppercase.
        self.assertEqual(
            updated_blog.blog_category_foreignkey.category_name,
            "Category For Create And Update Views",
        )
        self.assertEqual(updated_blog.blog_body, "This is an updated test blog.")
        self.assertEqual(updated_blog.blog_status, "draft")
        self.assertEqual(updated_blog.author.username, self.user.username)

    def test_update_blog_form_with_publish_button_clicked(self):

        """
        Test for a scenario where a blog is in drafts, but user updates it and moves it out from drafts and publishes it.
        """

        # Making blog a draft, so that when Publish button is clicked,
        # we can test if it's blog_status changed from 'draft' to 'published'
        self.update_form_data["blog_status"] = "draft"
        self.update_form_data["Publish"] = "Publish"

        response = self.client.post(
            reverse("update_blog", kwargs={"pk": self.blog.pk}),
            data=self.update_form_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 1)

        updated_blog = Blog.objects.last()
        self.assertEqual(updated_blog.blog_title, "Updated Test Blog")
        self.assertEqual(
            updated_blog.blog_category_foreignkey.category_name,
            "Category For Create And Update Views",
        )
        self.assertEqual(updated_blog.blog_body, "This is an updated test blog.")
        # Check if the status has changed from 'draft' to 'published'
        self.assertNotEqual(updated_blog.blog_status, "draft")
        self.assertEqual(updated_blog.author.username, self.user.username)

    def test_update_blog_form_with_save_as_draft_button_clicked(self):

        """
        Test for a scenario where a blog is in drafts, user updates it but does not intend to publish it.
        """

        # Making blog a draft, so that when Save as draft button is clicked,
        # we can test that it's blog_status has not changed.
        self.update_form_data["blog_status"] = "draft"
        self.update_form_data["Save as draft"] = "Save as draft"

        response = self.client.post(
            reverse("update_blog", kwargs={"pk": self.blog.pk}),
            data=self.update_form_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.count(), 1)

        updated_blog = Blog.objects.last()
        self.assertEqual(updated_blog.blog_title, "Updated Test Blog")
        # In the view we use title() method, so the catgory name will have first letters of each word as uppercase.
        self.assertEqual(
            updated_blog.blog_category_foreignkey.category_name,
            "Category For Create And Update Views",
        )
        self.assertEqual(updated_blog.blog_body, "This is an updated test blog.")
        # Check that status has not changed
        self.assertNotEqual(updated_blog.blog_status, "published")
        self.assertEqual(updated_blog.author.username, self.user.username)


class DeleteBlogViewFormTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

        # Creating non author user
        self.User = get_user_model()
        self.User.objects.create_user(
            email="not_an_author_user@email.com",
            username="not_an_author_user",
            password="not_an_author_user_password",
        )

    def test_delete_blog_form(self):
        response = self.client.post(reverse("delete_blog", kwargs={"pk": self.blog.pk}))
        no_response = self.client.get(
            reverse("delete_blog", kwargs={"pk": self.blog.pk})
        )
        pk_invalid = self.client.post("delete_blog", kwargs={"pk": "123456"})
        pk_does_not_exist = self.client.post(
            "delete_blog", kwargs={"pk": "00000000-0000-0000-0000-000000000000/"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(no_response.status_code, 404)
        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)
        self.assertEqual(Blog.objects.count(), 0)

    def test_delete_blog_form_for_logged_out_user(self):
        self.client.logout()
        delete_page_url = reverse("delete_blog", kwargs={"pk": self.blog.pk})

        response = self.client.post(delete_page_url)

        # User tries to access the delete page without being authenticated
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.last().blog_title, "Intermediate Python")
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={delete_page_url}"
        )

        # User gets redirected to login page
        response = self.client.get(f"{reverse('account_login')}?next={delete_page_url}")
        self.assertContains(response, "Welcome back")
        self.assertTemplateUsed(response, "account/login.html")

    def test_delete_blog_form_when_user_is_not_author(self):
        self.client.logout()
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )

        response = self.client.post(
            reverse("delete_blog", kwargs={"pk": self.blog.pk}),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.last().blog_title, "Intermediate Python")


class LikeBlogViewFormTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_like_functionality(self):
        # User click the like button
        response_for_like = self.client.post(
            reverse("like_blog", kwargs={"pk": self.blog.id})
        )
        self.assertEqual(response_for_like.status_code, 200)
        self.assertEqual(Blog.objects.get(id=self.blog.id).blog_likes_count, 1)

        # User clicks the like button again, resulting in unlike functionality
        response_for_unlike = self.client.post(
            reverse("like_blog", kwargs={"pk": self.blog.id})
        )
        self.assertEqual(response_for_unlike.status_code, 200)
        self.assertEqual(Blog.objects.get(id=self.blog.id).blog_likes_count, 0)

        # User likes a blog that does not exist or the primary key is invalid
        pk_invalid = self.client.post("like_blog", kwargs={"pk": "123456"})
        pk_does_not_exist = self.client.post(
            "like_blog", kwargs={"pk": "00000000-0000-0000-0000-000000000000/"}
        )

        self.assertEqual(pk_invalid.status_code, 404)
        self.assertEqual(pk_does_not_exist.status_code, 404)

        # User sends a GET request instead of a POST
        response = self.client.get(reverse("like_blog", kwargs={"pk": self.blog.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_like_functionality_for_logged_out_user(self):

        self.client.logout()
        like_url = reverse("like_blog", kwargs={"pk": self.blog.id})
        response = self.client.post(like_url)

        # User tries to like a blog without being authenticated
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.last().blog_likes_count, 0)
        self.assertRedirects(response, f"{reverse('account_login')}?next={like_url}")

        # User gets redirected to login page
        response = self.client.get(f"{reverse('account_login')}?next={like_url}")
        self.assertContains(response, "Welcome back")
        self.assertTemplateUsed(response, "account/login.html")


class ContactFormTests(TestCase):
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

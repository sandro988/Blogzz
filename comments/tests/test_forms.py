from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blogs.tests.test_forms import TestsData
from comments.models import Comment


class CreateCommentViewFormTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        self.form_data = {
            "comment_body": "First comment",
        }

    def test_create_comment_with_form_data(self):
        response = self.client.post(
            reverse("create_comment", kwargs={"pk": self.blog.pk}), data=self.form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("blog_detail", kwargs={"pk": self.blog.pk})
        )
        self.assertEqual(Comment.objects.count(), 1)

        new_comment = Comment.objects.get(comment_body="First comment")
        self.assertEqual(new_comment.blog, self.blog)
        self.assertEqual(new_comment.comment_author.email, "test_user@email.com")
        self.assertIsNone(new_comment.comment_parent)

    def test_create_comment_with_logged_out_user(self):
        self.client.logout()

        response = self.client.post(
            reverse("create_comment", kwargs={"pk": self.blog.pk}), data=self.form_data
        )

        self.assertEqual(response.status_code, 302)
        # Checking that no new comment has been created
        self.assertEqual(Comment.objects.count(), 0)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('create_comment', kwargs={'pk': self.blog.pk})}",
        )


class UpdateCommentViewFormTests(TestsData, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Creating non author user
        cls.User = get_user_model()
        cls.User.objects.create_user(
            email="not_an_author_user@email.com",
            username="not_an_author_user",
            password="not_an_author_user_password",
        )

        # Creating comment
        cls.comment = Comment.objects.create(
            blog=cls.blog,
            comment_author=cls.user,
            comment_body="First comment on 'Test blog'",
        )

        cls.form_data = {
            "comment_body": "Updated comment",
        }

        cls.form_data_from_non_author_user = {
            "comment_body": "I am not author of this comment",
        }

    def test_update_comment_with_form_data(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        response = self.client.post(
            reverse(
                "update_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            ),
            data=self.form_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("blog_detail", kwargs={"pk": self.blog.pk})
        )

        updated_comment = Comment.objects.last()
        self.assertEqual(updated_comment.comment_body, self.form_data["comment_body"])
        self.assertEqual(updated_comment.comment_author.email, "test_user@email.com")
        self.assertEqual(updated_comment.blog.pk, self.blog.pk)

    def test_update_comment_form_when_user_is_not_author(self):
        self.client.logout()
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )
        response = self.client.post(
            reverse(
                "update_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            ),
            data=self.form_data_from_non_author_user,
        )

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(
            Comment.objects.last().comment_body, "I am not author of this comment"
        )
        self.assertNotEqual(
            Comment.objects.last().comment_author.username,
            self.User.objects.last().username,
        )

    def test_update_comment_form_for_logged_out_user(self):
        self.client.logout()
        response = self.client.post(
            reverse(
                "update_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            ),
            data=self.form_data,
        )

        self.assertEqual(response.status_code, 302)
        # Checking that the comment was not updated
        self.assertNotEqual(Comment.objects.last().comment_body, "Updated comment")
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('update_comment', kwargs={'blog_pk': self.blog.pk, 'comment_pk': self.comment.pk})}",
        )

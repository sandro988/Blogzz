import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blogs.tests.test_forms import TestsData
from comments.models import Comment


class CommentTestsData(TestsData):
    """
    This class inherits everything from TestsData, as it is still useful in comment tests,
    Additionally, we are creating the data for testing the update and delete forms.
    """

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


class UpdateCommentViewFormTests(CommentTestsData, TestCase):
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


class DeleteCommentViewFormTests(CommentTestsData, TestCase):
    def test_delete_comment_form(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

        # Deleting the comment that exists
        response = self.client.post(
            reverse(
                "delete_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        # Deleting the comment that does not exist
        comment_does_not_exist_response = self.client.post(
            reverse(
                "delete_comment",
                kwargs={
                    "blog_pk": self.blog.pk,
                    "comment_pk": str(uuid.uuid4()),
                },
            )
        )

        # deleting the comment of a blog that does not exist
        blog_does_not_exist_response = self.client.post(
            reverse(
                "delete_comment",
                kwargs={
                    "blog_pk": str(uuid.uuid4()),
                    "comment_pk": self.comment.pk,
                },
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("blog_detail", kwargs={"pk": self.blog.pk})
        )
        self.assertEqual(
            Comment.objects.count(), 0
        )  # Checking that comment has been deleted
        self.assertEqual(comment_does_not_exist_response.status_code, 404)
        self.assertEqual(blog_does_not_exist_response.status_code, 404)

    def test_delete_comment_form_for_logged_out_user(self):
        comment_delete_page_url = reverse(
            "delete_comment",
            kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
        )

        response = self.client.post(comment_delete_page_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Comment.objects.last().comment_body, "First comment on 'Test blog'"
        )
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={comment_delete_page_url}"
        )

    def test_delete_comment_form_when_user_is_not_author(self):
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )
        comment_delete_page_url = reverse(
            "delete_comment",
            kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
        )

        response = self.client.post(comment_delete_page_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(
            Comment.objects.last().comment_body, "First comment on 'Test blog'"
        )


class UpvoteCommentViewFormTests(CommentTestsData, TestCase):
    def test_upvote_functionality(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

        # User upvotes the comment
        response_for_upvote = self.client.post(
            reverse(
                "upvote_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response_for_upvote.status_code, 200)
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 1)

        # User clicks the upvote button again which results in downvote
        response_for_downvote = self.client.post(
            reverse(
                "upvote_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )
        self.assertEqual(response_for_downvote.status_code, 200)
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 0)

        # User sends a GET request instead of a POST
        response = self.client.get(
            reverse(
                "upvote_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("blog_detail", kwargs={"pk": self.blog.pk})
        )

    def test_upvote_functionality_for_logged_out_user(self):
        response = self.client.post(
            reverse(
                "upvote_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('upvote_comment', kwargs={'blog_pk': self.blog.pk, 'comment_pk': self.comment.pk})}",
        )
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 0)

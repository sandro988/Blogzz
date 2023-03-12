from django.test import TestCase
from django.urls import reverse
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
            reverse("create_comment", kwargs={"pk": self.blog.pk}),
            data=self.form_data,
        )

        self.assertEqual(response.status_code, 302)
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

from django.test import TestCase
from django.urls import reverse
from blogs.tests.test_views import TestsData
from comments.models import Comment


class CreateCommentViewTests(TestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_create_comment_view(self):
        response = self.client.get(
            reverse("create_comment", kwargs={"pk": self.blog.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("blog_detail", kwargs={"pk": self.blog.pk})
        )

    def test_create_comment_with_logged_out_user(self):
        self.client.logout()

        response = self.client.get(
            reverse("create_comment", kwargs={"pk": self.blog.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('create_comment', kwargs={'pk': self.blog.pk})}",
        )


class CommentDetailViewTests(TestsData, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Creating comment
        cls.comment = Comment.objects.create(
            blog=cls.blog,
            comment_author=cls.user,
            comment_body="First comment on 'Test blog'",
        )

    def test_comment_detail_view(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        response = self.client.get(
            reverse("comment_detail", kwargs={"pk": self.comment.pk})
        )

        # Redirect to the blog_detail page and scroll down to the comment
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("blog_detail", kwargs={"pk": self.blog.pk})
            + f"#comment-{self.comment.pk}",
        )

    def test_comment_detail_view_with_logged_out_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("comment_detail", kwargs={"pk": self.comment.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('comment_detail', kwargs={'pk': self.comment.pk})}",
        )

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blogs.tests.test_views import TestsData
from comments.models import Comment


class CommentTestsData(TestsData):
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


class CommentDetailViewTests(CommentTestsData, TestCase):
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


class CreateCommentViewTests(CommentTestsData, TestCase):
    def setUp(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

    def test_create_comment_view(self):
        response = self.client.get(
            reverse("create_comment", kwargs={"blog_pk": self.blog.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")

    def test_create_reply_view(self):
        response = self.client.get(
            reverse(
                "create_reply",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")

    def test_create_comment_with_logged_out_user(self):
        self.client.logout()

        response = self.client.get(
            reverse("create_comment", kwargs={"blog_pk": self.blog.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('create_comment', kwargs={'blog_pk': self.blog.pk})}",
        )


class UpdateCommentViewTests(CommentTestsData, TestCase):
    def test_update_comment_view(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        response = self.client.get(
            reverse(
                "update_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")

    def test_update_comment_view_with_logged_out_user(self):
        self.client.logout()
        response = self.client.get(
            reverse(
                "update_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('update_comment', kwargs={'blog_pk': self.blog.pk, 'comment_pk': self.comment.pk})}",
        )

    def test_update_comment_view_with_non_author_user(self):
        self.client.logout()
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )
        response = self.client.get(
            reverse(
                "update_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, "blogs/blogs_detail.html")


class DeleteCommentViewTests(CommentTestsData, TestCase):
    def test_delete_comment_view(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        response = self.client.get(
            reverse(
                "delete_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "comments/delete_comment.html")

    def test_delete_comment_view_for_logged_out_user(self):
        response = self.client.get(
            reverse(
                "delete_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('delete_comment', kwargs={'blog_pk': self.blog.pk, 'comment_pk': self.comment.pk})}",
        )

    def test_delete_comment_view_for_non_author_user(self):
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )
        response = self.client.get(
            reverse(
                "delete_comment",
                kwargs={"blog_pk": self.blog.pk, "comment_pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, "comments/delete_comment.html")

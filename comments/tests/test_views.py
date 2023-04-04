import uuid
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

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "comments/comments_detail.html")

    def test_comment_detail_view_with_logged_out_user(self):
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
                kwargs={"pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")

    def test_update_comment_view_with_logged_out_user(self):
        self.client.logout()
        response = self.client.get(
            reverse(
                "update_comment",
                kwargs={"pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('update_comment', kwargs={'pk': self.comment.pk})}",
        )

    def test_update_comment_view_with_non_author_user(self):
        self.client.logout()
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )
        response = self.client.get(
            reverse(
                "update_comment",
                kwargs={"pk": self.comment.pk},
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
                kwargs={"pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "comments/delete_comment.html")

    def test_delete_comment_view_for_logged_out_user(self):
        response = self.client.get(
            reverse(
                "delete_comment",
                kwargs={"pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('delete_comment', kwargs={'pk': self.comment.pk})}",
        )

    def test_delete_comment_view_for_non_author_user(self):
        self.client.login(
            email="not_an_author_user@email.com", password="not_an_author_user_password"
        )
        response = self.client.get(
            reverse(
                "delete_comment",
                kwargs={"pk": self.comment.pk},
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, "comments/delete_comment.html")


class ContinueCommentThreadViewTests(CommentTestsData, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Creating ten nested replies for a comment
        for nested_reply in range(10):
            reply = Comment.objects.create(
                blog=cls.blog,
                comment_author=cls.user,
                comment_body=f"reply {nested_reply + 1}",
                comment_parent=Comment.objects.first(),
            )

    def test_blog_detail_view_contains_continue_thread_button(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        response = self.client.get(self.blog.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")
        self.assertContains(response, "Continue Thread")

        # Checking that the page contains comment with low depth and does not contain the comment that has depth more than 6.
        self.assertNotContains(response, "reply 7")
        self.assertContains(response, "reply 5")

    def test_continue_comment_thread_view(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        continue_thread_comment = Comment.objects.get(comment_body="reply 6")
        response = self.client.get(
            reverse(
                "continue_thread",
                kwargs={
                    "pk": continue_thread_comment.pk,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        # This page should not contain the 'Continue Thread' button, because there are only 11 comments total and
        # this page should contain 7th, 8th, 9th, 10th and 11nth comments, which means that the depth of the
        # comments on this page is not higher than 6.
        self.assertNotContains(response, "Continue Thread")
        # Checking that this page does not contain the 'continue_thread_comment' that we created above.
        self.assertNotContains(response, "reply 6")
        # Checking that this page contains replies of 'continue_thread_comment'.
        self.assertContains(response, "reply 7")

        # Checking that this view returns 404 if users pass the comment_pk that does not exist
        response = self.client.get(
            reverse(
                "continue_thread",
                kwargs={"pk": str(uuid.uuid4())},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_continue_comment_thread_view_for_logged_out_user(self):
        continue_thread_comment = Comment.objects.get(comment_body="reply 6")
        response = self.client.get(
            reverse(
                "continue_thread",
                kwargs={
                    "pk": continue_thread_comment.pk,
                },
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('continue_thread', kwargs={'pk': continue_thread_comment.pk,},)}",
        )

    def test_delete_comment_on_continue_comment_thread_view(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        continue_thread_comment = Comment.objects.get(comment_body="reply 6")

        # If for example we picked the comment with the body of reply 7, all of its child comments
        # would also be deleted, and that would result in redirect to blog_detail, not to the continue_thread page.
        # So here we are taking the 10th comment to test where will the user be redirected to after they delete this comment.
        comment_to_delete = Comment.objects.get(comment_body="reply 10")
        delete_comment_url = reverse(
            "delete_comment",
            kwargs={
                "pk": comment_to_delete.pk,
            },
        )

        response = self.client.post(
            delete_comment_url,
            {
                "next": reverse(
                    "continue_thread",
                    kwargs={
                        "pk": continue_thread_comment.pk,
                    },
                )
            },
        )

        # Checking that the comment does not exist anymore.
        self.assertFalse(Comment.objects.filter(pk=comment_to_delete.pk).exists())

        # Checking that we get redirected back to continue_thread page.
        self.assertRedirects(
            response,
            reverse(
                "continue_thread",
                kwargs={
                    "pk": continue_thread_comment.pk,
                },
            ),
        )

        # Deleting first and the only comment on continue_thread page
        comment_to_delete = Comment.objects.get(comment_body="reply 7")
        delete_comment_url = reverse(
            "delete_comment",
            kwargs={
                "pk": comment_to_delete.pk,
            },
        )

        response = self.client.post(
            delete_comment_url,
            {
                "next": reverse(
                    "continue_thread",
                    kwargs={
                        "pk": continue_thread_comment.pk,
                    },
                )
            },
        )

        # Checking that we get redirect to the blog_detail page and that the comment has been deleted
        self.assertRedirects(
            response, reverse("blog_detail", kwargs={"pk": self.blog.pk})
        )
        self.assertFalse(Comment.objects.filter(pk=comment_to_delete.pk).exists())

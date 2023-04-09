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
        self.reply_form_data = {"comment_body": "Reply to first comment"}

    def test_create_comment_with_form_data(self):
        response = self.client.post(
            reverse("create_comment", kwargs={"blog_pk": self.blog.pk}),
            data=self.form_data,
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

    def test_create_reply_with_form_data(self):
        # Creating parent comment
        response_for_comment = self.client.post(
            reverse("create_comment", kwargs={"blog_pk": self.blog.pk}),
            data=self.form_data,
        )
        parent_comment = Comment.objects.last().pk
        # Creating reply
        response_for_reply = self.client.post(
            reverse(
                "create_reply",
                kwargs={"comment_pk": parent_comment},
            ),
            data=self.reply_form_data,
        )

        self.assertEqual(response_for_reply.status_code, 302)
        self.assertRedirects(
            response_for_reply, reverse("blog_detail", kwargs={"pk": self.blog.pk})
        )
        self.assertEqual(Comment.objects.count(), 2)
        # Checking that reply's comment_parent was set correctly.
        self.assertEqual(Comment.objects.first().comment_parent, Comment.objects.last())

    def test_create_reply_with_invalid_parent_comment_pk(self):
        # Trying to create a parent comment and a reply to it.
        response_for_comment = self.client.post(
            reverse("create_comment", kwargs={"blog_pk": self.blog.pk}),
            data=self.form_data,
        )
        response_for_reply = self.client.post(
            reverse(
                "create_reply",
                kwargs={"comment_pk": str(uuid.uuid4())},
            ),
            data=self.reply_form_data,
        )

        self.assertEqual(response_for_reply.status_code, 404)
        # Checking that the reply has not been created
        self.assertEqual(Comment.objects.count(), 1)
        self.assertNotEqual(
            Comment.objects.last().comment_body, "Reply to first comment"
        )

    def test_create_comment_with_logged_out_user(self):
        self.client.logout()

        response = self.client.post(
            reverse("create_comment", kwargs={"blog_pk": self.blog.pk}),
            data=self.form_data,
        )

        self.assertEqual(response.status_code, 302)
        # Checking that no new comment has been created
        self.assertEqual(Comment.objects.count(), 0)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('create_comment', kwargs={'blog_pk': self.blog.pk})}",
        )


class UpdateCommentViewFormTests(CommentTestsData, TestCase):
    def test_update_comment_with_form_data(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        response = self.client.post(
            reverse(
                "update_comment",
                kwargs={"pk": self.comment.pk},
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
                kwargs={"pk": self.comment.pk},
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
                kwargs={"pk": self.comment.pk},
            ),
            data=self.form_data,
        )

        self.assertEqual(response.status_code, 302)
        # Checking that the comment was not updated
        self.assertNotEqual(Comment.objects.last().comment_body, "Updated comment")
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('update_comment', kwargs={'pk': self.comment.pk})}",
        )


class DeleteCommentViewFormTests(CommentTestsData, TestCase):
    def test_delete_comment_form(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

        # Deleting the comment that exists
        response = self.client.post(
            reverse(
                "delete_comment",
                kwargs={"pk": self.comment.pk},
            )
        )

        # Deleting the comment that does not exist
        comment_does_not_exist_response = self.client.post(
            reverse(
                "delete_comment",
                kwargs={
                    "pk": str(uuid.uuid4()),
                },
            )
        )

        # deleting the comment of a blog that does not exist
        blog_does_not_exist_response = self.client.post(
            reverse(
                "delete_comment",
                kwargs={
                    "pk": self.comment.pk,
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
            kwargs={"pk": self.comment.pk},
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
            kwargs={"pk": self.comment.pk},
        )

        response = self.client.post(comment_delete_page_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            Comment.objects.count(), 1
        )  # It is 11 because we have also created 10 replies in "CommentTestsData"
        self.assertEqual(
            Comment.objects.last().comment_body, "First comment on 'Test blog'"
        )


class VoteCommentViewFormTests(CommentTestsData, TestCase):
    def test_upvote_functionality(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

        # User upvotes the comment
        response_for_upvote = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"upvote-comment": "upvote"},
        )

        self.assertEqual(response_for_upvote.status_code, 200)
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 1)

        # User clicks the upvote button again
        response_for_downvote = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"upvote-comment": "upvote"},
        )
        self.assertEqual(response_for_downvote.status_code, 200)
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 0)

        # User sends a GET request instead of a POST
        response = self.client.get(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"upvote-comment": "upvote"},
        )
        self.assertEqual(response.status_code, 405)

    def test_upvote_functionality_for_logged_out_user(self):
        response = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"upvote-comment": "upvote"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('vote_comment', kwargs={'pk': self.comment.pk})}",
        )
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 0)

    def test_downvote_functionality(self):
        self.client.login(email="test_user@email.com", password="test_user_password")

        # User downvotes the comment
        response = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"downvote-comment": "downvote"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.last().comment_downvotes_count, 1)

        # User clicks the downvote button again
        response = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"downvote-comment": "downvote"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.last().comment_downvotes_count, 0)

        # User first upvotes the comment and than clicks the downvote button
        response_for_upvote = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"upvote-comment": "upvote"},
        )
        # Upvote increased by 1
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 1)

        response_for_downvote = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"downvote-comment": "downvote"},
        )
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 0)
        self.assertEqual(Comment.objects.last().comment_downvotes_count, 1)

    def test_downvote_functionality_for_logged_out_user(self):
        response = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"downvote-comment": "downvote"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('vote_comment', kwargs={'pk': self.comment.pk})}",
        )
        self.assertEqual(Comment.objects.last().comment_upvotes_count, 0)


class TestFormsOnContinueThreadView(CommentTestsData, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Creating ten nested replies for a comment
        for nested_reply in range(10):
            Comment.objects.create(
                blog=cls.blog,
                comment_author=cls.user,
                comment_body=f"reply {nested_reply + 1}",
                comment_parent=Comment.objects.first(),
            )

        cls.reply_form_data = {
            "comment_body": "Reply to comment on 'continue_thread' page"
        }

    def test_reply_functionality_on_continue_thread_view(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        continue_thread_comment = Comment.objects.get(comment_body="reply 6")
        parent_comment = Comment.objects.get(comment_body="reply 8")
        comment_reply_url = reverse(
            "create_reply", kwargs={"comment_pk": parent_comment.pk}
        )

        response = self.client.post(
            comment_reply_url,
            {
                "next": reverse(
                    "continue_thread",
                    kwargs={
                        "pk": continue_thread_comment.pk,
                    },
                ),
                **self.reply_form_data,
            },
        )

        self.assertEqual(response.status_code, 302)
        new_reply = Comment.objects.get(
            comment_body="Reply to comment on 'continue_thread' page"
        )
        self.assertIsNotNone(new_reply)
        self.assertEqual(
            new_reply.comment_body, "Reply to comment on 'continue_thread' page"
        )

        # Checking that we get redirected back to continue_thread page.
        self.assertRedirects(
            response,
            reverse("continue_thread", kwargs={"pk": continue_thread_comment.pk}),
        )

    def test_update_comment_on_continue_comment_thread_view(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        continue_thread_comment = Comment.objects.get(comment_body="reply 6")
        comment_to_update = Comment.objects.get(comment_body="reply 10")

        update_comment_url = reverse(
            "update_comment",
            kwargs={
                "pk": comment_to_update.pk,
            },
        )

        response = self.client.post(
            update_comment_url,
            {
                "next": reverse(
                    "continue_thread",
                    kwargs={
                        "pk": continue_thread_comment.pk,
                    },
                ),
                **self.form_data,
            },
        )

        self.assertEqual(response.status_code, 302)
        # Checking that the comment was updated.
        self.assertTrue(
            Comment.objects.get(pk=comment_to_update.pk).comment_body, "Updated comment"
        )
        # Checking that we get redirected back to continue_thread page.
        self.assertRedirects(
            response,
            reverse("continue_thread", kwargs={"pk": continue_thread_comment.pk}),
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


class SortCommentsFormTests(CommentTestsData, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.newer_comment = Comment.objects.create(
            blog=cls.blog,
            comment_author=cls.user,
            comment_body="Second comment on 'Test blog'",
        )

    def test_sorting_comments_by_oldest(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        blog_detail_url = reverse("blog_detail", kwargs={"pk": self.blog.pk})
        response = self.client.get(blog_detail_url, {"sort": "oldest"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")
        comments = response.context["comments"]
        self.assertEqual(comments[0], self.comment)
        self.assertEqual(comments[1], self.newer_comment)

    def test_sorting_comments_by_newest(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        blog_detail_url = reverse("blog_detail", kwargs={"pk": self.blog.pk})
        response = self.client.get(blog_detail_url, {"sort": "newest"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")
        comments = response.context["comments"]
        self.assertEqual(comments[0], self.newer_comment)
        self.assertEqual(comments[1], self.comment)

    def test_sorting_comments_by_popularity(self):
        self.client.login(email="test_user@email.com", password="test_user_password")
        # User upvotes the comment
        response_for_upvote = self.client.post(
            reverse(
                "vote_comment",
                kwargs={"pk": self.comment.pk},
            ),
            {"upvote-comment": "upvote"},
        )

        blog_detail_url = reverse("blog_detail", kwargs={"pk": self.blog.pk})
        response = self.client.get(blog_detail_url, {"sort": "popular"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blogs_detail.html")

        # We upvoted first comment, so it should be outputed first as it will have more upvotes than the second comment.
        comments = response.context["comments"]
        self.assertEqual(comments[0], self.comment)
        self.assertEqual(comments[1], self.newer_comment)

import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from blogs.models import Blog, Category
from blogs.tests.test_models import SetUpDataForBlogAndCommentModels
from comments.models import Comment


class CommentModelTests(SetUpDataForBlogAndCommentModels):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        # Creating comment
        cls.comment = Comment.objects.create(
            blog=cls.blog,
            comment_author=cls.user,
            comment_body="First comment on 'Test blog'",
        )


    def test_comment_model(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(
            Comment.objects.first().comment_body, "First comment on 'Test blog'"
        )
        self.assertEqual(str(self.comment), "First comment on 'Test blog'")
        self.assertTrue(Comment.objects.first().is_parent)

    def test_comment_model_for_replies(self):
        # Creating reply for comment that we created above
        reply = Comment.objects.create(
            blog=self.blog,
            comment_author=self.user,
            comment_body="First reply",
            comment_parent=self.comment,
        )

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(str(reply), "First reply")
        self.assertFalse(Comment.objects.first().is_parent)
        # Checking that the parent of this reply is the comment that we created in setUpTestData
        self.assertEqual(reply.comment_parent, self.comment)
        # Checking that the get_replies method of the Comment model functions correctly
        self.assertIn(reply, self.comment.get_replies())
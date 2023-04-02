import uuid
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from blogs.models import Blog


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    comment_author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment_body = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_updated = models.DateTimeField(auto_now=True)
    comment_parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    comment_upvotes = models.ManyToManyField(
        get_user_model(), related_name="upvote", default=None, blank=True
    )
    comment_upvotes_count = models.IntegerField(default="0")
    comment_downvotes = models.ManyToManyField(
        get_user_model(), related_name="downvote", default=None, blank=True
    )
    comment_downvotes_count = models.IntegerField(default="0")
    comment_depth = models.IntegerField(default=1)

    class Meta:
        ordering = ("-comment_created",)

    def save(self, *args, **kwargs):
        # If comment is a reply we get the depth of its parent comment and increase it by one
        if self.comment_parent is not None:
            self.comment_depth = self.comment_parent.comment_depth + 1
        super(Comment, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.comment_body[:50]

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"pk": self.blog.id})

    def get_replies(self):
        return Comment.objects.filter(comment_parent=self).order_by("comment_created")

    @property
    def is_parent(self):
        return self.comment_parent is None

    def upvote_comment(self, user):
        if user in self.comment_upvotes.all():
            self.comment_upvotes.remove(user)
            self.comment_upvotes_count -= 1
        elif user in self.comment_downvotes.all():
            self.comment_downvotes.remove(user)
            self.comment_downvotes_count -= 1
            self.comment_upvotes.add(user)
            self.comment_upvotes_count += 1
        else:
            self.comment_upvotes.add(user)
            self.comment_upvotes_count += 1

        self.save()

    def downvote_comment(self, user):
        if user in self.comment_upvotes.all():
            self.comment_upvotes.remove(user)
            self.comment_upvotes_count -= 1
            self.comment_downvotes.add(user)
            self.comment_downvotes_count += 1
        elif user in self.comment_downvotes.all():
            self.comment_downvotes.remove(user)
            self.comment_downvotes_count -= 1
        else:
            self.comment_downvotes.add(user)
            self.comment_downvotes_count += 1
        self.save()

    def count_comments_and_replies(self):
        """
        This method recursively counts the number of comments and their replies.
        """

        count = 0

        for reply in self.replies.all():
            count += 1
            count += reply.count_comments_and_replies()

        return count

    def get_reply_count(self):
        return self.replies.count()

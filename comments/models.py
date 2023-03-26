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
    # Did not implement 'comment_downvotes_count' because i only need to keep track of the number of upvotes
    comment_downvotes = models.ManyToManyField(
        get_user_model(), related_name="downvote", default=None, blank=True
    )
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

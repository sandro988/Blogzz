from django.contrib.auth import get_user_model
from django.db import models
from blogs.models import Blog

# Create your models here.


class Comment(models.Model):
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

    class Meta:
        ordering = ("-comment_created",)

    def __str__(self) -> str:
        return self.comment_body[:50]

    def get_replies(self):
        return Comment.objects.filter(comment_parent=self).order_by("comment_created")

    @property
    def is_parent(self):
        return self.comment_parent is None

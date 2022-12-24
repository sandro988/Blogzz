import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.category_name


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=200)
    blog_category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    blog_body = models.TextField()
    blog_created = models.DateTimeField(auto_now_add=True)
    blog_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.blog_title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"pk": self.id})

from urllib.parse import urlencode
from django.urls import reverse_lazy
from .utils import get_comment_from_next_url


class SuccessUrlMixin:
    def get_success_url(self):
        next = self.request.POST.get("next")
        sort_param = self.request.POST.get("sort")

        if next:
            url = self.redirect_to_continue_thread_page(next)
        else:
            url = self.get_detail_url()

        if sort_param:
            query_params = urlencode({"sort": sort_param})
            url = f"{url}?{query_params}"

        return url

    def redirect_to_continue_thread_page(self, next: str):
        comment = get_comment_from_next_url(next)
        return reverse_lazy(
            "continue_thread",
            kwargs={"pk": comment.pk},
        )

    def get_detail_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.get_object().blog.id})

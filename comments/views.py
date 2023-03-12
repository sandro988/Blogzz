from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from blogs.models import Blog, Category
from .models import Comment
from .forms import CommentForm


class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = "blogs/blogs_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        blog = self.object.blog
        url = blog.get_absolute_url() + f"#comment-{self.object.pk}"
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()[:10]
        context["popular_blogs"] = Blog.get_popular_blogs()
        context["form"] = CommentForm()
        context["blog"] = self.blog
        return context


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blogs/blogs_detail.html"
    login_url = "account_login"

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.blog_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):

        """
        Retrieves the blog post for the given ID, and ensures that the user has navigated to
        the current page from a previous page. If the user has not navigated to the current
        page from a previous page, for example by typing the url directly into the browser,
        the user is redirected back to the blog_detail page for the appropriate blog post.
        """

        blog = get_object_or_404(Blog, pk=self.kwargs["pk"])
        if not self.request.META.get("HTTP_REFERER"):
            return redirect("blog_detail", pk=self.kwargs["pk"])

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.kwargs["pk"]})

from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from blogs.models import Blog, Category
from .models import Comment
from .forms import CommentCreationForm, CommentUpdateForm


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
        context["create_page_form"] = CommentCreationForm()
        context["blog"] = self.blog
        return context


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreationForm
    template_name = "blogs/blogs_detail.html"
    login_url = "account_login"

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.blog_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = get_object_or_404(Blog, pk=self.kwargs["pk"])
        context["create_page_form"] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.kwargs["pk"]})


class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = "blogs/blogs_detail.html"
    login_url = "account_login"

    def form_valid(self, form):
        form.instance.blog_id = self.kwargs["blog_pk"]

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = self.get_object().blog
        context["comment_to_be_updated"] = self.get_object()
        context["update_page_form"] = self.get_form()
        context["create_page_form"] = CommentCreationForm()
        return context

    def get_object(self, queryset=None):
        blog_pk = self.kwargs["blog_pk"]
        comment_pk = self.kwargs["comment_pk"]
        comment = get_object_or_404(Comment, pk=comment_pk, blog_id=blog_pk)
        return comment

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.kwargs["blog_pk"]})

    def get_template_names(self):
        if self.request.htmx:
            return "comments/update_comment.html"
        return "blogs/blogs_detail.html"

    def test_func(self):
        object = self.get_object()
        return object.comment_author == self.request.user


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Blog
    template_name = "comments/delete_comment.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = self.get_object().blog
        context["comment_to_be_deleted"] = self.get_object()
        context["create_page_form"] = CommentCreationForm()
        return context

    def get_object(self, queryset=None):
        blog_pk = self.kwargs["blog_pk"]
        comment_pk = self.kwargs["comment_pk"]
        comment = get_object_or_404(Comment, pk=comment_pk, blog_id=blog_pk)
        return comment

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.kwargs["blog_pk"]})

    def get_template_names(self):
        if self.request.htmx:
            return "comments/delete_comment.html"
        return "blogs/blogs_detail.html"

    def test_func(self):
        object = self.get_object()
        return object.comment_author == self.request.user

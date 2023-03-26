from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from blogs.models import Blog
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
        context["create_page_form"] = CommentForm()
        context["blog"] = self.blog
        return context


class CreateCommentView(LoginRequiredMixin, CreateView):
    """
    View implemented for creating new comments or replies to already existing comments.
    """

    model = Comment
    form_class = CommentForm
    template_name = "blogs/blogs_detail.html"
    login_url = "account_login"

    def get_object(self, queryset=None):
        # If the request will come from a 'reply_comment' then we get the parent comment
        # and use it in form_valid as a parent of reply, but if the request comes from a
        # 'create_comment' then we set the parent comment to None.

        blog = get_object_or_404(Blog, pk=self.kwargs["blog_pk"])
        result = {"blog": blog, "comment": None}
        if self.kwargs.get("comment_pk"):
            parent_comment = get_object_or_404(
                Comment, pk=self.kwargs["comment_pk"], blog_id=self.kwargs["blog_pk"]
            )
            result["comment"] = parent_comment

        return result

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.blog_id = self.kwargs["blog_pk"]
        form.instance.comment_parent = self.get_object().get("comment")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = self.get_object().get("blog")
        context["comment"] = self.get_object().get("comment")
        context["create_page_form"] = self.get_form()

        return context

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.kwargs["blog_pk"]})

    def get_template_names(self):
        if self.request.htmx:
            return "comments/reply_to_comment.html"

        return "blogs/blogs_detail.html"


class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
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
        context["create_page_form"] = CommentForm()
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
        context["create_page_form"] = CommentForm()
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


class UpvoteCommentView(LoginRequiredMixin, View):
    template_name = "comments/upvote_downvote_comment.html"

    def post(self, request, *args, **kwargs):
        blog_pk = kwargs["blog_pk"]
        comment_pk = kwargs["comment_pk"]
        user = request.user
        comment = get_object_or_404(Comment, pk=comment_pk, blog_id=blog_pk)

        if user in comment.comment_upvotes.all():
            comment.comment_upvotes.remove(user)
            comment.comment_upvotes_count -= 1
        elif user in comment.comment_downvotes.all():
            comment.comment_downvotes.remove(user)
            comment.comment_upvotes.add(user)
            comment.comment_upvotes_count += 1
        else:
            comment.comment_upvotes.add(user)
            comment.comment_upvotes_count += 1

        comment.save()

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):
        return redirect("blog_detail", pk=kwargs["blog_pk"])

    def get_context_data(self, **kwargs):
        context = {}
        comment_pk = kwargs["comment_pk"]
        blog_pk = kwargs["blog_pk"]
        comment = get_object_or_404(Comment, pk=comment_pk, blog_id=blog_pk)
        context["comment"] = comment
        context["blog"] = comment.blog
        context["upvote_count"] = comment.comment_upvotes_count
        return context


class DownvoteCommentView(UpvoteCommentView):
    def post(self, request, *args, **kwargs):
        blog_pk = kwargs["blog_pk"]
        comment_pk = kwargs["comment_pk"]
        user = request.user
        comment = get_object_or_404(Comment, pk=comment_pk, blog_id=blog_pk)

        if user in comment.comment_upvotes.all():
            comment.comment_upvotes.remove(user)
            comment.comment_downvotes.add(user)
            comment.comment_upvotes_count -= 1
        elif user in comment.comment_downvotes.all():
            comment.comment_downvotes.remove(user)
            comment.comment_upvotes_count += 1
        else:
            comment.comment_downvotes.add(user)
            comment.comment_upvotes_count -= 1

        comment.save()

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)


class ContinueCommentThreadView(LoginRequiredMixin, DetailView):
    """
    This view is used to display the continuation of a comment thread when the depth of the replies exceeds 6.
    Depth refers to the number of levels of replies to a comment.

    Functionality:
        - Fetches the comment with a depth greater than 6 using the 'comment_pk' and 'blog_pk' URL parameters.
        - Passes the 'continue_thread_comment' object to the context, which is then used in the 'list_comments'
        template to display only the replies to this comment.
        - Renders the 'blogs/blogs_detail.html' template with the 'CommentForm' for creating new comments.

    Example Usage:
        - A comment has 10 levels of replies.
        - The blog page displays the first 6 levels of replies and a 'Continue Thread' button.
        - Clicking on the 'Continue Thread' button redirects the user to this view, which displays the remaining 4 levels of replies to that comment.
    """

    model = Comment
    template_name = "blogs/blogs_detail.html"

    def get_object(self, queryset=None):
        continue_thread_comment = get_object_or_404(
            Comment, pk=self.kwargs["comment_pk"], blog_id=self.kwargs["blog_pk"]
        )

        return continue_thread_comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["continue_thread_comment"] = self.get_object()
        context["blog"] = self.get_object().blog
        context["create_page_form"] = CommentForm()
        return context

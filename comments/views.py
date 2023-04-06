from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.http import Http404
from blogs.models import Blog
from .models import Comment
from .forms import CommentForm
from .utils import get_comment_from_next_url


class CommentDetailView(LoginRequiredMixin, DetailView):
    """
    View implemented for displaying the details of a single comment, this includes the comment
    itself and all of its nested replies. It inherits from LoginRequiredMixin to ensure that only
    authenticated users can access the view.

    Methods:
        get_context_data: Adds extra context to the view, we are adding a form for creating comments and a blog to which the comment belongs.
        get_template_names: Returns the appropriate template based on whether the request is made via HTMX or not.
    """

    model = Comment
    context_object_name = "comment"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_page_form"] = CommentForm()
        context["blog"] = self.get_object().blog
        return context

    def get_template_names(self):
        if self.request.htmx:
            return "comments/list_comments.html"
        return "comments/comments_detail.html"


class CreateCommentView(LoginRequiredMixin, CreateView):
    """
    View implemented for creating new comments or replies to already existing comments.
    It inherits from LoginRequiredMixin to ensure that only authenticated users can access the view.

    Methods:
        get_object: Retrieves the parent comment or blog associated with the request. If
            the request came from a "create_reply" url, it returns the parent comment and its associated blog, while
            if it came from a "create_comment" form, it returns just the associated blog. Returns a dictionary with the
            keys "blog" and "comment".
        form_valid: Creates a new comment and assigns its author and parent blog/comment.
            Redirects the user to the "get_success_url()" method on success.
        get_context_data: Adds context variables to the view's template context. Adds the
            associated blog and parent comment to the context, as well as the "CommentForm" form for creating
            new comments and continue_thread_url variable, which will be used to determine where should users be redirected
            if they replied to a comment from "continue_thread" page.
        get_success_url: Returns the URL to redirect to after a successful comment creation. In this
            case, it redirects the user to the "blog_detail" view for the associated blog.
        get_template_names: Returns the appropriate template based on whether the request is made via HTMX or not.

    Raises:
        django.http.Http404: If the associated blog or parent comment cannot be found.
    """

    model = Comment
    form_class = CommentForm
    login_url = "account_login"

    def get_object(self):
        result = {"blog": None, "comment": None}

        if self.kwargs.get("blog_pk"):
            blog = get_object_or_404(Blog, pk=self.kwargs["blog_pk"])
            result["blog"] = blog
        elif self.kwargs.get("comment_pk"):
            parent_comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
            result["comment"] = parent_comment
            result["blog"] = parent_comment.blog

        return result

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.blog_id = self.get_object().get("blog").id
        form.instance.comment_parent = self.get_object().get("comment")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = self.get_object().get("blog")
        context["comment"] = self.get_object().get("comment")
        context["create_page_form"] = self.get_form()
        context["continue_thread_url"] = self.request.GET.get("next")

        return context

    def get_success_url(self):
        next = self.request.POST.get("next")

        if next:
            comment = get_comment_from_next_url(next)
            return reverse_lazy(
                "continue_thread",
                kwargs={"pk": comment.pk},
            )

        return reverse_lazy(
            "blog_detail", kwargs={"pk": self.get_object().get("blog").id}
        )

    def get_template_names(self):
        if self.request.htmx:
            return "comments/reply_to_comment.html"

        return "blogs/blogs_detail.html"


class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View implemented for letting users to update their own comments. It inherits from LoginRequiredMixin
    to ensure that only authenticated users can access the view, and from
    UserPassesTestMixin to ensure that only the comment author can delete a comment.

    Methods:
        get_context_data: Adds extra context to the view, we are adding the blog to which the comment belongs to, the comment to be updated,
            forms for updating the comment and creating the comment, and continue_thread_url which will be used if user clicks on edit button
            on "continue_thread" page, so that after they edit a comment they get redirected back to the "continue_thread" page and not blog_detail page.
        get_success_url: Returns the URL to redirect to after a successful update of a comment.
        get_template_names: Returns the appropriate template based on whether the request is made via HTMX or not.
        test_func: Checks if the current user is the author of the comment being updated.
    """

    model = Comment
    form_class = CommentForm
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = self.get_object().blog
        context["comment_to_be_updated"] = self.get_object()
        context["update_page_form"] = self.get_form()
        context["create_page_form"] = self.get_form()
        context["continue_thread_url"] = self.request.GET.get("next")

        return context

    def get_success_url(self):
        next = self.request.POST.get("next")

        if next:
            comment = get_comment_from_next_url(next)
            return reverse_lazy(
                "continue_thread",
                kwargs={"pk": comment.pk},
            )

        return reverse_lazy("blog_detail", kwargs={"pk": self.get_object().blog.id})

    def get_template_names(self):
        if self.request.htmx:
            return "comments/update_comment.html"
        return "blogs/blogs_detail.html"

    def test_func(self):
        object = self.get_object()
        return object.comment_author == self.request.user


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View implemented for letting users to delete their own comments. It inherits from LoginRequiredMixin
    to ensure that only authenticated users can access the view, and from
    UserPassesTestMixin to ensure that only the comment author can delete a comment.

    Methods:
        get_context_data: We are passing blog to which the comment belongs, the comment to be deleted, form for creating the comment,
            url to "continue_thread" page(this can be a URL or None, depending on from where the user makes a GET request, if user clicks on delete
            button from "continue_thread" page than this variable will be a URL, but if users clicks on the delete button from "blog_detail" page than it will
            be None) and at last we are adding the comment of "continue_thread"(this is the comment that has the depth of 6, so it is the last comment that will
            be shown on "blog_detail" page, we are using this variable in templates to determine how many replies and nested replies it has).
        get_success_url: Returns the URL to redirect to after a successful comment deletion. If the request was made from continue_thread page
            it will redirect users back to the "continue_thread" page, otherwise they will be redirected to "blog_detail" page.
        get_template_names: Returns the appropriate template based on whether the request is made via HTMX or not.
        test_func: Checks if the current user is the author of the comment being deleted.
        redirect_to_continue_thread_page: This method determines where the user should be redirected if they deleted comment on "continue_thread" page.

    Returns:
        The view renders a confirmation page to the user, asking them to confirm the deletion of
        the comment. If the user confirms the deletion, the comment is deleted and the user is
        redirected to the appropriate page.
    """

    model = Comment
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = self.get_object().blog
        context["comment_to_be_deleted"] = self.get_object()
        context["create_page_form"] = CommentForm()
        context["continue_thread_url"] = self.request.GET.get("next")

        # We are using this context variable to determine how many replies does the continue_thread comment have, so that when user
        # deletes one of them we can determine if we should add hx-push-url parameter to the form or not in the delete_comment.html template.
        # If the comment that user wants to delete is the only reply of continue_thread_comment with or without its own replies than we add
        # hx-push-url parameter to the delete form.
        context["continue_thread_comment"] = get_comment_from_next_url(
            self.request.GET.get("next")
        )

        return context

    def get_success_url(self):
        next = self.request.POST.get("next")
        if next:
            return self.redirect_to_continue_thread_page(next, self.get_object())

        return reverse_lazy("blog_detail", kwargs={"pk": self.get_object().blog.id})

    def get_template_names(self):
        if self.request.htmx:
            return "comments/delete_comment.html"
        return "blogs/blogs_detail.html"

    def test_func(self):
        object = self.get_object()
        return object.comment_author == self.request.user

    def redirect_to_continue_thread_page(self, url: str, comment_to_delete: Comment):

        continue_thread_comment = get_comment_from_next_url(url)
        # Number of replies and nested replies on 'continue_thread' page.
        continue_thread_comment_replies = (
            continue_thread_comment.count_comments_and_replies()
        )

        # If the comment that user inteds to delete is the only comment on "continue_thread" page
        # and it is the first reply of continue_thread_comment we delete the comment and redirect to "blog_detail" page
        # otherwise we redirect back to "continue_thread" page.

        if (
            comment_to_delete == continue_thread_comment.get_replies().first()
            and continue_thread_comment.get_reply_count() == 1
        ):
            return reverse_lazy("blog_detail", kwargs={"pk": self.get_object().blog.id})

        return reverse_lazy(
            "continue_thread",
            kwargs={"pk": continue_thread_comment.pk},
        )


class CommentVoteView(LoginRequiredMixin, View):
    """
    View implemented for letting users to upvote and downvote comments. It inherits from LoginRequiredMixin
    to ensure that only authenticated users can access the view and this view allows only POST request.

    Methods:
        get_object: Fetches the comment object from the URL parameter 'pk'.
        get_context_data: We are passing a comment that will be upvoted or downvoted and a blog to which the comment belongs.
        post: This method Handles the POST request and upvotes/downvotes the comment accordingly using upvote_comment/downvote_comment methods
            defined in Comment model.
    """

    template_name = "comments/upvote_downvote_comment.html"
    login_url = "account_login"
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        user = request.user
        comment = self.get_object()

        if request.POST.get("upvote-comment"):
            comment.upvote_comment(user)
        elif request.POST.get("downvote-comment"):
            comment.downvote_comment(user)

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

    def get_object(self):
        comment_pk = self.kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=comment_pk)

        return comment

    def get_context_data(self, **kwargs):
        context = {}
        comment = self.get_object()
        context["comment"] = comment
        context["blog"] = comment.blog
        return context


class ContinueCommentThreadView(LoginRequiredMixin, DetailView):
    """
    View implemented for showing comments that otherwise wont fit on the "blog_detail" page.
    This view is used to display the continuation of a comment thread when the depth of the replies exceeds 6.
    Depth refers to the number of levels of replies to a comment.

    Functionality:
        - Fetches the comment with a depth greater than 6.
        - Passes the 'continue_thread_comment' object to the context, which is then used in the 'list_comments'
        template to display only the replies to that comment.
        - Raises a 404 error if the comment has no replies and user tries to still access the continue_thread page of that comment.

    Example Usage:
        - A comment has 10 levels of replies.
        - The blog page displays the first 6 levels of replies and a 'Continue Thread' button.
        - Clicking on the 'Continue Thread' button redirects the user to this view, which displays the remaining 4 levels of replies to that comment.
    """

    model = Comment
    login_url = "account_login"

    def get(self, request, *args, **kwargs):
        if self.get_object().replies.count() == 0:
            raise Http404("This comment has no replies.")

        return super().get(request, *args, **kwargs)

    def get_object(self):
        continue_thread_comment = get_object_or_404(Comment, pk=self.kwargs["pk"])

        return continue_thread_comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["continue_thread_comment"] = self.get_object()
        context["blog"] = self.get_object().blog
        context["create_page_form"] = CommentForm()
        return context

    def get_template_names(self):
        if self.request.htmx:
            return "comments/list_comments.html"
        return "blogs/blogs_detail.html"

from .models import Blog, Category


def popular_categories_and_blogs(request):
    categories = Category.objects.all()[:10]
    popular_blogs = Blog.get_popular_blogs()

    return {"categories": categories, "popular_blogs": popular_blogs}

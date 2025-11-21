from django.views.generic import ListView
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "articles.html"
    paginate_by = 25
    ordering = ('-write_date')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(is_active=True,)
        return context
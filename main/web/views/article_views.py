from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from ...models import Article
from ..forms.article_forms import ArticleForm, ArticleSearchForm
from ...api.controllers.auth_controller import AdminRequiredMixin


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'kidology/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.all()
        form = ArticleSearchForm(self.request.GET)

        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            search_in_title = form.cleaned_data.get('search_in_title')
            search_in_content = form.cleaned_data.get('search_in_content')
            categories = form.cleaned_data.get('categories')
            age_groups = form.cleaned_data.get('age_groups')

            if search_query:
                query = Q()
                if search_in_title:
                    query |= Q(title__icontains=search_query)
                if search_in_content:
                    query |= Q(content__icontains=search_query)
                if query:
                    queryset = queryset.filter(query)

            if categories:
                queryset = queryset.filter(categories__in=categories).distinct()
            if age_groups:
                queryset = queryset.filter(age_groups__in=age_groups).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ArticleSearchForm(self.request.GET)
        return context

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'kidology/article_detail.html'

class ArticleCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Article
    template_name = 'kidology/article_form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        # Najpierw zapisz artykuł bez relacji many-to-many
        self.object = form.save(commit=False)
        self.object.save()

        # Teraz możesz zapisać relacje many-to-many
        form.save_m2m()

        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Article
    template_name = 'kidology/article_form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('article_list')

class ArticleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Article
    template_name = 'kidology/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')

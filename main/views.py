from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Article
from .forms import ArticleForm, CustomUserCreationForm, CustomAuthenticationForm, ArticleSearchForm
from .api.repositories.article_repository import ArticleRepository
from .api.services.article_service import ArticleService
from .api.controllers.article_controller import ArticleController
from .api.repositories.auth_repository import AuthRepository
from .api.services.auth_service import AuthService
from .api.controllers.auth_controller import AuthController
class AuthViewSet(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = AuthRepository()
        service = AuthService(repository)
        self.controller = AuthController(service)

    @action(detail=False, methods=['post'])
    def login(self, request):
        return self.controller.login(request)

    @action(detail=False, methods=['post'])
    def register(self, request):
        return self.controller.register(request)
class ArticleViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = ArticleRepository()
        service = ArticleService(repository)
        self.controller = ArticleController(service)

    def list(self, request):
        return self.controller.get_articles(request)

    def retrieve(self, request, pk=None):
        return self.controller.get_article(request, pk)

    def create(self, request):
        return self.controller.create_article(request)

    def update(self, request, pk=None):
        return self.controller.update_article(request, pk)

    def destroy(self, request, pk=None):
        return self.controller.delete_article(request, pk)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'kidology/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Rejestracja zakończona pomyślnie. Możesz się teraz zalogować.')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'kidology/login.html'
    # success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        messages.success(self.request, 'Zalogowano pomyślnie.')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Niepoprawny adres e-mail lub hasło.')
        return super().form_invalid(form)

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

class ArticleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Article
    template_name = 'kidology/article_form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('article_list')

class ArticleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Article
    template_name = 'kidology/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')


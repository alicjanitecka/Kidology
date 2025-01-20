from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .api.views.article_view import ArticleViewSet
from .api.views.auth_view import AuthViewSet
from .web.views.article_views import (
    ArticleListView, ArticleDetailView, ArticleCreateView,
    ArticleUpdateView, ArticleDeleteView
)
from .web.views.auth_views import SignUpView, CustomLoginView


router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    # path('login/', CustomLoginView.as_view(template_name='kidology/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),  # usuń template_name z .as_view()

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]

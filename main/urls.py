from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/new/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='kidology/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]

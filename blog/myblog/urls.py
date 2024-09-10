from django.urls import path
from .views import list_articles, create_article, edit_article, delete_article, articles_by_category, articles_by_tag, article_detail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', list_articles, name='articles'),
    path('formulaire/', create_article, name='formulaire'),
    
    # Routes pour filtrer les articles par catégorie et tag
    path('articles/category/<int:category_id>/', articles_by_category, name='articles_by_category'),
    path('articles/tag/<int:tag_id>/', articles_by_tag, name='articles_by_tag'),
    
    # Route pour les détails d'un article
    path('articles/<int:article_id>/', article_detail, name='article_detail'),

    # Routes pour modifier et supprimer un article
    path('articles/edit/<int:article_id>/', edit_article, name='edit_article'),
    path('articles/delete/<int:article_id>/', delete_article, name='delete_article'),
    
]
